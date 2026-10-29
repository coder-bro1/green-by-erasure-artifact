"""Replay the P4 judge on logged pilot failures with new prompt variants, and score all variants.

The judged cases are rebuilt from the logged judge_v1 prompts (same specification, test and observed
behaviour), so every variant sees exactly the inputs v1 saw. Ground truth: a judged failure is a real
bug when its generated test REVEALS the bug (passes on the fixed version); otherwise the test is wrong.

Lives outside src/ and prompts/ on purpose: those files are fingerprinted by gbe.runner, and changing
them would block resuming a pilot that is still running.

  replay:  python analysis/judge_replay.py replay --run phase1_pilot --variant v2a
  score:   python analysis/judge_replay.py score --run phase1_pilot [--run ...]
"""
import argparse
import collections
import csv
import hashlib
import json
import sys
import time
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.llm import OPTIONS, http, local_model  # noqa: E402
from gbe.policies import judge_parse  # noqa: E402

PROMPTS = {'v2a': ROOT / 'analysis/prompts/judge_v2a.txt', 'v2b': ROOT / 'analysis/prompts/judge_v2b.txt'}
MARKERS = ('Specification (signature and docstring):\n', '\nTest (contains its expected values):\n',
           '\nObserved behaviour:\n', '\nReturn only JSON:')


def text_of(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        if 'message' in x:
            return (x['message'] or {}).get('content', '')
        if 'messages' in x:
            return '\n'.join(m.get('content', '') for m in x['messages'])
    if isinstance(x, list):
        return '\n'.join(text_of(i) for i in x)
    return ''


def split_v1_prompt(prompt):
    s, t, o, r = (prompt.index(m) for m in MARKERS)
    return {'spec': prompt[s + len(MARKERS[0]):t], 'test': prompt[t + len(MARKERS[1]):o],
            'feedback': prompt[o + len(MARKERS[2]):r]}


def parse_json(text):
    raw = text
    for fence in ('```json', '```'):
        if fence in raw:
            raw = raw.split(fence, 1)[1].split('```', 1)[0]
            break
    start, end = raw.find('{'), raw.rfind('}')
    try:
        return json.loads(raw[start:end + 1]) if 0 <= start < end else None
    except ValueError:
        return None


def verdict(variant, text):
    if variant == 'v1':
        # Score v1 exactly as P4 acted on it in the runs (the harness parser also requires a reason).
        return judge_parse(text)['verdict']
    value = parse_json(text) or {}
    if variant == 'v2b':
        return {'YES': 'BUG', 'NO': 'TEST_WRONG', 'UNCLEAR': 'UNSURE'}.get(value.get('answer'), 'UNSURE')
    v = value.get('verdict')
    return v if v in ('BUG', 'TEST_WRONG', 'UNSURE') else 'UNSURE'


def cases(run):
    run_dir = ROOT / 'runs' / run
    labels = {(r['test_id']): r for r in csv.DictReader(open(run_dir / 'tests.csv', encoding='utf-8'))
              if r['stage'] == 'GEN'}
    out = []
    for line in open(run_dir / 'llm_calls.jsonl', encoding='utf-8'):
        c = json.loads(line)
        if c.get('purpose') != 'judge':
            continue
        g = labels[c['test_id']]
        out.append({'test_id': c['test_id'], 'condition': g['condition'], 'gen_input': g['gen_input'],
                    'gen_label': g['label'], 'fields': split_v1_prompt(text_of(c['prompt'])),
                    'v1_response': text_of(c.get('response'))})
    return out


def replay(run, variant):
    run_dir = ROOT / 'runs' / run
    manifest = json.loads((run_dir / 'manifest.json').read_text(encoding='utf-8'))
    progress = json.loads((run_dir / 'progress.json').read_text(encoding='utf-8'))
    if progress['percent'] < 100:
        raise SystemExit(f'{run} is still running ({progress["percent"]}%); replay only finished runs.')
    model, pinned = manifest['model'], manifest['model_digest']
    local_model(model, pinned)  # refuses cloud tags and digest changes
    template = PROMPTS[variant].read_text(encoding='utf-8')
    out_dir = run_dir / 'judge_replay'
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f'{variant}.jsonl'
    done = {json.loads(l)['test_id'] for l in open(out_path, encoding='utf-8')} if out_path.exists() else set()
    todo = [c for c in cases(run) if c['test_id'] not in done]
    total, started = len(done) + len(todo), time.monotonic()
    with open(out_path, 'a', encoding='utf-8') as fh:
        for i, case in enumerate(todo, 1):
            prompt = template.format(**case['fields'])
            request = {'model': model, 'stream': False, 'think': False, 'options': OPTIONS,
                       'messages': [{'role': 'user', 'content': prompt}]}
            t0 = time.monotonic()
            try:
                response = http('/api/chat', request)
            except urllib.error.HTTPError as error:
                body = error.read().decode('utf-8', 'replace')
                # Same rule as gbe.llm: a deterministic repeat-limit abort becomes an empty answer
                # (verdict UNSURE); every other server error stops the replay.
                if error.code != 500 or 'repeat limit' not in body:
                    raise
                response = {'message': {'role': 'assistant', 'content': ''}, 'aborted_error': body}
            text = response['message']['content']
            fh.write(json.dumps({'test_id': case['test_id'], 'variant': variant, 'model': model,
                                 'model_digest': pinned, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
                                 'template_sha256': hashlib.sha256(template.encode()).hexdigest(),
                                 'response': text, 'verdict': verdict(variant, text),
                                 'reasoning_returned': bool(response['message'].get('thinking')),
                                 'aborted': 'aborted_error' in response,
                                 'duration_s': time.monotonic() - t0,
                                 'timestamp': datetime.now(timezone.utc).isoformat()}) + '\n')
            fh.flush()
            n = len(done) + i
            eta = (time.monotonic() - started) / i * (total - n)
            (out_dir / f'{variant}_progress.json').write_text(json.dumps(
                {'done': n, 'total': total, 'percent': round(100 * n / total, 2), 'eta_seconds': round(eta),
                 'updated': datetime.now(timezone.utc).isoformat()}), encoding='utf-8')
            print(f'\r{run} {variant}: {n}/{total} ({100 * n / total:.1f}%), ETA {eta / 60:.1f} min   ', end='', flush=True)
    print()


def metrics(rows):
    out = {'n': len(rows), 'verdicts': dict(collections.Counter(r['verdict'] for r in rows))}
    buggy = [r for r in rows if r['condition'] == 'buggy']
    fixed = [r for r in rows if r['condition'] == 'fixed']
    for name, keep in (('strict', ('BUG',)), ('default', ('BUG', 'UNSURE'))):
        tp = sum(r['verdict'] in keep and r['gen_label'] == 'REVEALS' for r in buggy)
        fp = sum(r['verdict'] in keep and r['gen_label'] != 'REVEALS' for r in buggy)
        fn = sum(r['verdict'] not in keep and r['gen_label'] == 'REVEALS' for r in buggy)
        fa = sum(r['verdict'] in keep for r in fixed)
        out[name] = {'buggy_tp': tp, 'buggy_fp': fp, 'buggy_fn': fn,
                     'precision': round(tp / (tp + fp), 3) if tp + fp else None,
                     'recall': round(tp / (tp + fn), 3) if tp + fn else None,
                     'fixed_false_alarms': fa, 'fixed_failures': len(fixed),
                     'fixed_false_alarm_rate': round(fa / len(fixed), 3) if fixed else None}
    return out


def score(runs):
    report = {}
    for run in runs:
        base = cases(run)
        variants = {'v1': [dict(c, verdict=verdict('v1', c['v1_response'])) for c in base]}
        for v in PROMPTS:
            path = ROOT / 'runs' / run / 'judge_replay' / f'{v}.jsonl'
            if path.exists():
                got = {json.loads(l)['test_id']: json.loads(l)['verdict'] for l in open(path, encoding='utf-8')}
                variants[v] = [dict(c, verdict=got[c['test_id']]) for c in base if c['test_id'] in got]
        report[run] = {v: metrics(rows) for v, rows in variants.items()}
    out = ROOT / 'review' / 'out' / 'judge_replay_scores.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1), encoding='utf-8')
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=('replay', 'score'))
    p.add_argument('--run', action='append', required=True)
    p.add_argument('--variant', choices=sorted(PROMPTS))
    a = p.parse_args()
    if a.action == 'replay':
        for run in a.run:
            replay(run, a.variant)
    else:
        score(a.run)
