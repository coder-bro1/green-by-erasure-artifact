"""S5: audit of a real tool, CoverUp 0.6.3, on the Phase 2 pairs (docs/PHASE2_SPEC.md 8.8).

For every HumanEvalFix and QuixBugs pair of the main runs, both versions: CoverUp runs on the program alone
(package `prog`, module `solution`), with Qwen2.5-Coder 7B through the frozen Ollama, temperature 0, prompt
family gpt-v1 (the default gpt-v2 offers a tool that the local model calls with invented names, which
crashes CoverUp), up to 3 attempts per segment, no test isolation and no repeats (Windows), and the
Windows temporary-file patch in patches/coverup-0.6.3-windows-tempfile.txt. CoverUp keeps a test only if it
passes and adds coverage; on any error it asks the model to "Modify the test to correct it".

Every test version the model proposed (from CoverUp's log, in order) and every test CoverUp kept is then run
by the harness executor on both original versions and labelled REVEALS, ENCODES, NEUTRAL or BROKEN. Imports
of `prog.solution` are rewritten to `solution` for that execution only.

  python scripts/s5_coverup.py --only Python/27 --conditions buggy   one trial
  python scripts/s5_coverup.py                                         everything (resumable)
  python scripts/s5_coverup.py --config configs/s5_sensitivity.json    the predefined sensitivity rerun (stage B-1)
Results: runs/s5_coverup/results.jsonl (one record per program version), progress.json; CoverUp working
folders in .scratch/s5 (not in git). Run it only while no other model run uses the GPU.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import all_tasks, benchmark_name, program  # noqa: E402
from gbe.evaluate import label  # noqa: E402
from gbe.execute import execute  # noqa: E402
from gbe.util import now, read_json, write_json  # noqa: E402

COVERUP = ROOT / '.venv-coverup' / 'Scripts' / 'coverup.exe'
OUT = ROOT / 'runs' / 's5_coverup'
WORK = ROOT / '.scratch' / 's5'
MODEL = 'ollama/qwen2.5-coder:7b-instruct'
MAX_TOKENS = 2048
NO_THINK = False
LIMIT_S = 900


def run_coverup(folder):
    # PYTHONPATH must not be set: CoverUp prepends the source parent with ':' (POSIX), which on Windows turns
    # an existing PYTHONPATH into one invalid entry and makes `prog` unimportable in its own test runs (the
    # first 145 runs of 15 October were discarded for this). QuixBugs' node.py goes next to the package
    # instead (run_one), where CoverUp's own path entry already reaches it.
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env.update(OLLAMA_API_BASE='http://localhost:11434', PYTEST_ADDOPTS='-p no:isolate', GBE_COVERUP_MAX_TOKENS=str(MAX_TOKENS),
               GBE_COVERUP_NO_THINK='1' if NO_THINK else '0')
    command = [str(COVERUP), '--package-dir', 'src/prog', '--tests-dir', 'tests', '--model', MODEL,
               '--model-temperature', '0', '--prompt', 'gpt-v1', '--max-attempts', '3', '--log-file', 'coverup-log',
               '--checkpoint', 'coverup-ckpt.json', '--no-repeat-tests', '--no-isolate-tests']
    with open(folder / 'stdout.txt', 'wb') as out:
        process = subprocess.Popen(command, cwd=folder, env=env, stdout=out, stderr=subprocess.STDOUT)
        try:
            return process.wait(timeout=LIMIT_S)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            process.wait()
            return 'TIME_LIMIT'


def parse_log(text):
    """Model answers in order, as (segment, code) pairs, from CoverUp's log blocks.

    The code is what CoverUp itself runs (coverup.py, extract_python): the text after the first ```python line
    up to a closing fence or, for an answer cut off by the token cap, to the end. An answer without a ```python
    block gets code None: CoverUp gives up on it without running anything. (The first version of this function
    also accepted a bare ``` fence and otherwise kept the whole answer, fence included; analysis/s5_summary.py
    relabels the 161 answers where that differs.)"""
    answers = []
    for header, body in re.findall(r'---- \S+ (.+?) ----\n(\{.*?\n\})\n', text, flags=re.S):
        try:
            block = json.loads(body)
        except ValueError:
            continue
        for choice in block.get('choices', []):
            content = (choice.get('message') or {}).get('content') or ''
            m = re.search(r'```python\n(.*?)(?:```|\Z)', content, flags=re.S) if '```python' in content else None
            answers.append({'segment': header.strip(), 'code': m.group(1) if m else None})
    return answers


def for_execution(code):
    """The harness executor puts the program in solution.py and support modules next to it, without the
    package: `from prog.X import`, `import prog.X` and `from prog import X` become plain module imports."""
    code = re.sub(r'\bfrom\s+prog\.(\w+)\s+import\b', r'from \1 import', code)
    code = re.sub(r'\bfrom\s+prog\s+import\s+', 'import ', code)
    code = re.sub(r'\bimport\s+prog\.(\w+)', r'import \1', code)
    return re.sub(r'\bprog\.(solution|node)\b', r'\1', code)


def labelled(task, code):
    versions = {c: program(task, c) for c in ('fixed', 'buggy')}
    outcomes = {c: execute(versions[c], '', for_execution(code), timeout=10, support=task.get('support'))['outcome']
                for c in versions}
    return outcomes, label(outcomes['fixed'], outcomes['buggy'])


def run_one(task, condition):
    key = f"{task['task_id'].replace('/', '_')}__{condition}"
    folder = WORK / key
    if folder.exists():
        shutil.rmtree(folder)
    (folder / 'src' / 'prog').mkdir(parents=True)
    (folder / 'tests').mkdir()
    (folder / 'src' / 'prog' / '__init__.py').write_bytes(b'')
    (folder / 'src' / 'prog' / 'solution.py').write_text(program(task, condition), encoding='utf-8')
    for name, text in (task.get('support') or {}).items():
        # The program does `from node import Node`: a top-level module, so it sits in src/, which CoverUp
        # puts on the path. It stays outside the package so CoverUp targets only the program under test.
        (folder / 'src' / name).write_text(text, encoding='utf-8')
    t0 = time.monotonic()
    status = run_coverup(folder)
    seconds = round(time.monotonic() - t0, 1)
    log = (folder / 'coverup-log').read_text(encoding='utf-8', errors='replace') if (folder / 'coverup-log').exists() else ''
    answers = parse_log(log)
    for a in answers:
        a['outcomes'], a['label'] = labelled(task, a['code']) if a['code'] is not None else ({}, 'NO_CODE')
    kept = []
    for f in sorted((folder / 'tests').glob('test_coverup_*.py')):
        code = f.read_text(encoding='utf-8')
        outcomes, lab = labelled(task, code)
        kept.append({'file': f.name, 'code': code, 'outcomes': outcomes, 'label': lab})
    return {'pair_id': task['task_id'], 'benchmark': benchmark_name(task), 'condition': condition, 'status': status,
            'seconds': seconds, 'gave_up': log.count('Too many attempts, giving up'), 'answers': answers,
            'kept': kept, 'finished': now()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--conditions', nargs='*', default=['buggy', 'fixed'])
    ap.add_argument('--config', help='JSON with model, max_tokens, out, work and pairs (a rerun on a fixed selection)')
    a = ap.parse_args()
    global MODEL, MAX_TOKENS, NO_THINK, OUT, WORK
    only = set(a.only or [])
    if a.config:
        cfg = read_json(ROOT / a.config)
        MODEL, MAX_TOKENS, NO_THINK = cfg['model'], int(cfg['max_tokens']), not cfg.get('think', True)
        OUT, WORK = ROOT / cfg['out'], ROOT / cfg['work']
        only = (only & set(cfg['pairs'])) if only else set(cfg['pairs'])  # --only narrows the configured pairs
    used = {p['pair_id'] for p in read_json(ROOT / 'runs' / 'phase2_qwen25_code' / 'pairs.json')}
    tasks = [t for t in all_tasks()[0] if t['task_id'] in used and (not only or t['task_id'] in only)]
    OUT.mkdir(parents=True, exist_ok=True)
    results = OUT / 'results.jsonl'
    done = set()
    if results.exists():
        done = {(r['pair_id'], r['condition']) for r in map(json.loads, results.read_text(encoding='utf-8').splitlines())}
    jobs = [(t, c) for c in a.conditions for t in tasks if (t['task_id'], c) not in done]
    total = len(jobs) + len(done)
    with open(results, 'a', encoding='utf-8') as fh:
        for i, (task, condition) in enumerate(jobs, 1):
            record = run_one(task, condition)
            fh.write(json.dumps(record) + '\n')
            fh.flush()
            os.fsync(fh.fileno())
            labels = [x['label'] for x in record['answers']]
            write_json(OUT / 'progress.json', {'done': len(done) + i, 'total': total,
                                               'percent': round(100 * (len(done) + i) / total, 1), 'updated': now()})
            print(f"{len(done) + i}/{total} {task['task_id']} {condition}: {record['status']}, {len(labels)} answers "
                  f"{labels}, kept {[k['label'] for k in record['kept']]}", flush=True)


if __name__ == '__main__':
    main()
