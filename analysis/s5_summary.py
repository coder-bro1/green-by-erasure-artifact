"""S5 review and summary: what CoverUp 0.6.3 does with the bug-revealing tests its model writes.

Inputs: runs/s5_coverup/results.jsonl (scripts/s5_coverup.py) and CoverUp's own logs in .scratch/s5/<key>/coverup-log.

Review checks:
- one record per pair and version, CoverUp exit status, answers without code;
- alignment: the answers in the record are the model responses of the log, in order;
- CoverUp's own verdict on every answer, read from what follows it in the log for the same segment (an error
  message asking to "Modify the test to correct it", a "still lacks coverage" message, a passing pytest run and
  "Saved as", or a give-up line), against the harness executor's outcome on the same version;
- every kept test passes on the version CoverUp ran on;
- the code of each answer is what CoverUp runs (scripts/s5_coverup.py, parse_log, after the fix of 16 October):
  answers whose stored code differs (a truncated block, which the first parser kept with its fence) are
  re-executed on both versions (cached in runs/s5_coverup/relabel.json); answers without a ```python block are
  NO_CODE, never run by CoverUp, and left out of the labels;
- answers with a TIMEOUT outcome (10 s) are re-executed at 30 s on both versions (cached in
  runs/s5_coverup/timeout_recheck.json) and relabelled, as for the main runs.
Fates: a segment of a buggy program "had evidence" when one of its answers reveals the bug (passes on the fixed,
fails on the buggy version). Its fate is INVERTED when CoverUp then keeps an answer of that segment that encodes
the bug, NEUTRALIZED when it keeps one that passes on both versions, and DROPPED when it keeps none. A revealing
test cannot be kept on a buggy program, since CoverUp keeps only passing tests.
Writes review/out/s5_coverup.md. Usage: python analysis/s5_summary.py
With --config configs/s5_sensitivity.json it reviews the sensitivity rerun instead (its own output and work folders)
and writes review/out/s5_sensitivity.md.
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'analysis'))
from gbe.benchmarks import all_tasks, program  # noqa: E402
from gbe.evaluate import label  # noqa: E402
from gbe.execute import execute  # noqa: E402
from s5_coverup import for_execution, parse_log  # noqa: E402
from memlimit import cap  # noqa: E402

OUT = ROOT / 'runs' / 's5_coverup'
WORK = ROOT / '.scratch' / 's5'
HEADER = re.compile(r'^---- \S+ (.+?) ----$', re.M)


def blocks(text):
    heads = list(HEADER.finditer(text))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        yield h.group(1).strip(), text[h.end():end].strip()


def verdicts(text):
    """CoverUp's verdict on each model response of the log, in order."""
    items = list(blocks(text))
    out = []
    for i, (seg, body) in enumerate(items):
        if not body.startswith('{'):
            continue
        try:
            block = json.loads(body)
        except ValueError:
            continue
        if 'choices' not in block:
            continue
        v = 'NONE'
        for b in [b for s, b in items[i + 1:] if s == seg]:
            if 'Saved as' in b:
                v = 'ACCEPTED'
                break
            if b.startswith('{'):
                try:
                    last = json.loads(b)['messages'][-1]['content']
                except (ValueError, KeyError, IndexError):
                    last = ''
                v = ('FAIL' if last.startswith('Executing the test yields an error') else
                     'PASS_NO_COVERAGE' if last.startswith('This test still lacks coverage') else 'OTHER')
                break
            if 'No Python code' in b:
                v = 'NO_CODE'
                break
            if 'Too many attempts' in b or b.strip() == 'giving up':
                v = 'GAVE_UP'
                break
            if 'measure_coverage timed out' in b:
                v = 'COVERAGE_TIMEOUT'
                break
        out.append(v)
    return out


def sha(code):
    return hashlib.sha1(code.encode('utf-8')).hexdigest()[:12]


def run_both(task, code, timeout):
    outcomes = {c: execute(program(task, c), '', for_execution(code), timeout=timeout, support=task.get('support'))['outcome']
                for c in ('fixed', 'buggy')}
    return {'outcomes': outcomes, 'label': label(outcomes['fixed'], outcomes['buggy'])}


def relabel(records, tasks):
    """Answers as CoverUp runs them; returns the number re-executed and the number of NO_CODE answers."""
    path = OUT / 'relabel.json'
    cache = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    redone = no_code = 0
    for r in records:
        log = WORK / f"{r['pair_id'].replace('/', '_')}__{r['condition']}" / 'coverup-log'
        parsed = parse_log(log.read_text(encoding='utf-8', errors='replace'))
        assert len(parsed) == len(r['answers']), (r['pair_id'], r['condition'])
        for i, (a, p) in enumerate(zip(r['answers'], parsed)):
            if p['code'] is None:
                a['code'], a['outcomes'], a['label'] = None, {}, 'NO_CODE'
                no_code += 1
                continue
            if p['code'] == a['code']:
                continue
            key = f"{r['pair_id']}|{r['condition']}|{i}|{sha(p['code'])}"
            if key not in cache:
                cache[key] = run_both(tasks[r['pair_id']], p['code'], 10)
                path.write_text(json.dumps(cache, indent=1), encoding='utf-8')
            a['code'], a['outcomes'], a['label'] = p['code'], cache[key]['outcomes'], cache[key]['label']
            redone += 1
    return redone, no_code


def recheck(records, tasks):
    path = OUT / 'timeout_recheck.json'
    cache = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    for r in records:
        for kind in ('answers', 'kept'):
            for i, a in enumerate(r[kind]):
                if a['code'] is None or 'TIMEOUT' not in a['outcomes'].values():
                    continue
                key = f"{r['pair_id']}|{r['condition']}|{kind}|{i}|{sha(a['code'])}"
                if key not in cache:
                    cache[key] = run_both(tasks[r['pair_id']], a['code'], 30)
                    path.write_text(json.dumps(cache, indent=1), encoding='utf-8')
                a['outcomes_10s'], a['label_10s'] = a['outcomes'], a['label']
                a['outcomes'], a['label'] = cache[key]['outcomes'], cache[key]['label']
    return cache


def main():
    global OUT, WORK
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--config')
    a = ap.parse_args()
    report = 's5_coverup.md'
    title_extra = ''
    if a.config:
        cfg = json.loads((ROOT / a.config).read_text(encoding='utf-8'))
        OUT, WORK = ROOT / cfg['out'], ROOT / cfg['work']
        report = 's5_sensitivity.md'
        title_extra = f" (sensitivity rerun: {cfg['model']}, {cfg['max_tokens']}-token cap, think={cfg.get('think', True)})"
    cap()
    tasks = {t['task_id']: t for t in all_tasks()[0]}
    records = [json.loads(line) for line in (OUT / 'results.jsonl').read_text(encoding='utf-8').splitlines()]
    # Keys of the first recheck (16 October) lacked the code hash; they belong to the stored code.
    tpath = OUT / 'timeout_recheck.json'
    if tpath.exists():
        old = json.loads(tpath.read_text(encoding='utf-8'))
        if any(k.count('|') == 3 for k in old):
            byid = {(r['pair_id'], r['condition']): r for r in records}
            new = {}
            for k, v in old.items():
                if k.count('|') == 3:
                    pair, cond, kind, i = k.split('|')
                    k = f"{k}|{sha(byid[(pair, cond)][kind][int(i)]['code'])}"
                new[k] = v
            tpath.write_text(json.dumps(new, indent=1), encoding='utf-8')
    redone, no_code = relabel(records, tasks)
    cache = recheck(records, tasks)
    changed = sum(1 for r in records for k in ('answers', 'kept') for a in r[k] if 'label_10s' in a and a['label_10s'] != a['label'])
    model = cfg['model'] if a.config else 'ollama/qwen2.5-coder:7b-instruct'
    lines = ['# S5: CoverUp 0.6.3 audit', '',
             f'Computed by `analysis/s5_summary.py` from `{OUT.relative_to(ROOT).as_posix()}/results.jsonl` and',
             f"CoverUp's logs. Model {model} through the frozen Ollama, temperature 0, prompt family gpt-v1.", '',
             '## Review', '']
    keys = Counter((r['pair_id'], r['condition']) for r in records)
    lines.append(f"- Records: {len(records)}, one per pair and version: {all(v == 1 for v in keys.values())}; "
                 f"{Counter(r['condition'] for r in records)}; benchmarks {dict(Counter(r['benchmark'] for r in records))}.")
    lines.append(f"- CoverUp exit status: {dict(Counter(str(r['status']) for r in records))}; total time "
                 f"{sum(r['seconds'] for r in records) / 3600:.1f} h, longest run {max(r['seconds'] for r in records):.0f} s.")
    # Verdicts and alignment.
    agree, misaligned, vcount = Counter(), [], Counter()
    for r in records:
        log = WORK / f"{r['pair_id'].replace('/', '_')}__{r['condition']}" / 'coverup-log'
        v = verdicts(log.read_text(encoding='utf-8', errors='replace')) if log.exists() else []
        if len(v) != len(r['answers']):
            misaligned.append(r['pair_id'] + ' ' + r['condition'])
            v = ['UNALIGNED'] * len(r['answers'])
        for a, verdict in zip(r['answers'], v):
            a['verdict'] = verdict
            vcount[verdict] += 1
            if a['code'] is None:
                continue
            ours = a['outcomes'][r['condition']] == 'PASS'
            if verdict == 'FAIL':
                agree[('CoverUp: fails', 'ours: passes' if ours else 'ours: fails')] += 1
            elif verdict in ('ACCEPTED', 'PASS_NO_COVERAGE'):
                agree[('CoverUp: passes', 'ours: passes' if ours else 'ours: fails')] += 1
        accepted = sum(a.get('verdict') == 'ACCEPTED' for a in r['answers'])
        if accepted != len(r['kept']):
            r['accepted_mismatch'] = (accepted, len(r['kept']))
    n_answers = sum(len(r['answers']) for r in records)
    lines.append(f"- Model answers: {n_answers}; records whose answers do not line up with the log: {len(misaligned)}"
                 + (f" ({', '.join(misaligned[:5])})" if misaligned else '') + '.')
    lines.append(f"- CoverUp's verdict per answer: {dict(vcount)}.")
    lines.append('- Agreement of the executor with CoverUp on the version CoverUp ran on: '
                 + '; '.join(f'{a}, {b}: {n}' for (a, b), n in sorted(agree.items())) + '.')
    mism = [r for r in records if 'accepted_mismatch' in r]
    lines.append(f"- Kept tests: {sum(len(r['kept']) for r in records)}; records where accepted answers and kept files differ "
                 f"in number: {len(mism)}; kept tests that pass on their own version: "
                 f"{sum(k['outcomes'][r['condition']] == 'PASS' for r in records for k in r['kept'])}.")
    lines.append(f"- Answers re-executed with the code CoverUp ran (truncated blocks): {redone}; answers without a python "
                 f"block (CoverUp gave up without running them, left out below): {no_code}.")
    lines.append(f"- Time-out recheck at 30 s: {len(cache)} executions, {changed} label changes.")
    lines.append(f"- Answers by label: {dict(Counter(a['label'] for r in records for a in r['answers'] if a['code'] is not None))}; "
                 f"kept tests by version and label: {dict(Counter((r['condition'], k['label']) for r in records for k in r['kept']))}.")
    lines.append('')
    # Fates on buggy programs, per segment that had evidence.
    lines += ['## What CoverUp does with bug evidence', '']
    rows = []
    for bench in ('HumanEvalFix', 'QuixBugs', 'all'):
        rs = [r for r in records if bench in ('all', r['benchmark'])]
        buggy = [r for r in rs if r['condition'] == 'buggy']
        fixed = [r for r in rs if r['condition'] == 'fixed']
        fates, after = Counter(), Counter()
        sig_prog, fb_prog, inv_prog = set(), set(), set()
        for r in buggy:
            segs = defaultdict(list)
            for a in r['answers']:
                segs[a['segment']].append(a)
            for seg, ans in segs.items():
                idx = [i for i, a in enumerate(ans) if a['label'] == 'REVEALS']
                if not idx:
                    continue
                sig_prog.add(r['pair_id'])
                kept = [a for a in ans[idx[0] + 1:] if a.get('verdict') == 'ACCEPTED']
                fate = ('DROPPED' if not kept else 'INVERTED' if kept[-1]['label'] == 'ENCODES' else
                        'NEUTRALIZED' if kept[-1]['label'] == 'NEUTRAL' else 'KEPT_' + kept[-1]['label'])
                fates[fate] += 1
                if fate == 'INVERTED':
                    inv_prog.add(r['pair_id'])
                for i in idx:
                    if i + 1 < len(ans):
                        after[ans[i + 1]['label']] += 1
                    else:
                        after['no further answer'] += 1
            if any(k['label'] == 'ENCODES' for k in r['kept']):
                fb_prog.add(r['pair_id'])
        n_seg = sum(fates.values())
        reg = sum(any(k['label'] == 'REVEALS' for k in r['kept']) for r in fixed)
        fixed_sig = sum(any(a['label'] == 'REVEALS' for a in r['answers']) for r in fixed)
        rows.append((bench, len(buggy), len(sig_prog), n_seg, fates, after, len(fb_prog), len(inv_prog), len(fixed), fixed_sig, reg,
                     sum(bool(r['kept']) for r in buggy), sum(bool(r['kept']) for r in fixed)))
    lines += ['| Programs | Buggy programs | With a bug-revealing answer | Segments with evidence | Dropped | Inverted | Neutralized | Reported | Buggy programs with a fix-blocking kept test | Correct programs | With a bug-revealing answer | Kept suite reveals the bug (regression test) |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for bench, nb, sig, nseg, fates, after, fb, inv, nf, fsig, reg, kb, kf in rows:
        lines.append(f"| {bench} | {nb} | {sig} | {nseg} | {fates['DROPPED']} | {fates['INVERTED']} | {fates['NEUTRALIZED']} | 0 | {fb} | {nf} | {fsig} | {reg} |")
    allrow = rows[-1]
    lines += ['', f"- The next answer after a bug-revealing answer (CoverUp has sent the failure and asked for a correction): "
              f"{dict(allrow[5])}.",
              f"- Programs with any kept test: buggy {allrow[11]} of {allrow[1]}, correct {allrow[12]} of {allrow[8]}.",
              f"- Other fates: {dict((k, v) for k, v in allrow[4].items() if k not in ('DROPPED', 'INVERTED', 'NEUTRALIZED'))}.", '']
    lines[0] += title_extra
    out = ROOT / 'review' / 'out' / report
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
