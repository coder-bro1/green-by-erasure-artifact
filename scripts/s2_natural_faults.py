"""S2: natural LLM faults from HumanEval+ (docs/PHASE2_SPEC.md 8.8; settings in configs/s2_natural.json).

  python scripts/s2_natural_faults.py expected   reference outputs of the canonical solutions (CPU)
  python scripts/s2_natural_faults.py generate   the local models write solutions at temperature 0.8 (GPU)
  python scripts/s2_natural_faults.py filter     run every candidate: HumanEval's tests and HumanEval+ inputs (CPU)
  python scripts/s2_natural_faults.py select     one fault per task -> data/s2/natural_faults.json

Every step is resumable. Candidate programs are model-written code; they run in their own process at
below-normal priority under a private temporary folder, with a time limit. The generation prompt lives in
configs/s2_natural_prompt.txt (not in prompts/, so the harness fingerprint of the queued runs is untouched).
"""
import argparse
import ast
import gzip
import hashlib
import json
import math
import os
import pickle
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.util import now, read_json, write_json  # noqa: E402

CONFIG = read_json(ROOT / 'configs' / 's2_natural.json')
OUT = ROOT / 'runs' / 's2_natural'
EXPECTED = ROOT / 'data' / 'raw' / 'humanevalplus_v0.1.10' / 'expected'
BELOW_NORMAL = 0x4000

RUNNER = r'''
import copy, importlib, pickle, sys
sys.setrecursionlimit(10000)
inputs = pickle.load(open(sys.argv[1], 'rb'))
fn = getattr(importlib.import_module('solution'), sys.argv[3])
out = []
for args in inputs:
    try:
        out.append(('ok', fn(*copy.deepcopy(args))))
    except BaseException as e:  # noqa: BLE001 - every failure is data here
        out.append(('error', type(e).__name__))
try:
    pickle.dump(out, open(sys.argv[2], 'wb'))
except Exception:  # an unpicklable result counts as a crash
    pickle.dump([('error', 'Unpicklable')] * len(inputs), open(sys.argv[2], 'wb'))
'''


def tasks():
    path = ROOT / CONFIG['dataset']['file']
    if hashlib.sha256(path.read_bytes()).hexdigest() != CONFIG['dataset']['sha256']:
        raise SystemExit('HumanEval+ file differs from the pinned sha256')
    with gzip.open(path, 'rt', encoding='utf-8') as fh:
        rows = [json.loads(line) for line in fh]
    if len(rows) != 164:
        raise SystemExit(f'Expected 164 tasks, got {len(rows)}')
    return rows


def private_tmp():
    parent = ROOT / '.scratch' / 's2' / str(os.getpid())
    parent.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=parent)


def run_inputs(source, entry_point, inputs, timeout):
    """Call the function on every input in a separate process; return [(status, value)] or 'TIMEOUT'."""
    with private_tmp() as d:
        Path(d, 'solution.py').write_text(source, encoding='utf-8')
        Path(d, 'runner.py').write_text(RUNNER, encoding='utf-8')
        pickle.dump(inputs, open(Path(d, 'in.pkl'), 'wb'))
        try:
            subprocess.run([sys.executable, 'runner.py', 'in.pkl', 'out.pkl', entry_point], cwd=d, timeout=timeout,
                           capture_output=True, creationflags=BELOW_NORMAL if os.name == 'nt' else 0)
        except subprocess.TimeoutExpired:
            return 'TIMEOUT'
        if not Path(d, 'out.pkl').exists():
            return 'CRASH'
        return pickle.load(open(Path(d, 'out.pkl'), 'rb'))


def same(a, b, atol):
    """Python equality, as HumanEval's own assertions use, with a tolerance for floats (also inside lists
    and tuples). A list and a tuple differ, as they do under ==; True and 1 are equal, as they are under ==."""
    if isinstance(a, float) or isinstance(b, float):
        try:
            return math.isclose(a, b, rel_tol=1e-6, abs_tol=max(atol, 1e-6))
        except TypeError:
            return False
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(same(x, y, atol) for x, y in zip(a, b))
    try:
        return bool(a == b)
    except Exception:  # noqa: BLE001 - an uncomparable result counts as different
        return False


def all_inputs(task):
    return list(task['base_input']) + list(task['plus_input'])


def expected():
    EXPECTED.mkdir(parents=True, exist_ok=True)
    for i, task in enumerate(tasks()):
        path = EXPECTED / (task['task_id'].replace('/', '_') + '.pkl')
        if path.exists():
            continue
        result = run_inputs(task['prompt'] + task['canonical_solution'], task['entry_point'], all_inputs(task),
                            timeout=600)
        if not isinstance(result, list) or any(s != 'ok' for s, _ in result):
            raise SystemExit(f"Canonical solution of {task['task_id']} failed: {result if not isinstance(result, list) else 'error'}")
        pickle.dump([v for _, v in result], open(path, 'wb'))
        print(f"{i + 1}/164 {task['task_id']}: {len(result)} reference outputs", flush=True)


def extract(response, task):
    """Build the buggy program: the task's prompt, the body of the model's function, and its other code."""
    text = response
    if '```' in text:
        parts = text.split('```')
        blocks = [parts[i] for i in range(1, len(parts), 2)]
        text = next((b for b in blocks if f"def {task['entry_point']}" in b), blocks[0] if blocks else '')
        text = text[len('python'):] if text.startswith('python') else text
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    entry = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == task['entry_point']), None)
    if entry is None:
        return None
    lines = text.split('\n')
    body = entry.body
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], 'value', None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    if not body:
        return None
    body_text = textwrap.dedent('\n'.join(lines[body[0].lineno - 1:entry.end_lineno]))
    prompt_names = {n.name for n in ast.parse(task['prompt']).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    extra = [ast.get_source_segment(text, n) for n in tree.body
             if n is not entry and not (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in prompt_names)
             and isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef, ast.Assign))]
    program = task['prompt'].rstrip('\n') + '\n' + textwrap.indent(body_text, '    ') + '\n'
    if extra:
        program += '\n\n' + '\n\n'.join(extra) + '\n'
    try:
        ast.parse(program)
    except SyntaxError:
        return None
    return program


def generate():
    from gbe.llm import Client
    models = read_json(ROOT / 'configs' / 'models.json')['models']
    g = CONFIG['generation']
    rows = tasks()
    out = OUT / 'candidates_raw.jsonl'
    done = set()
    if out.exists():
        done = {(r['task_id'], r['model'], r['seed']) for r in map(json.loads, out.read_text(encoding='utf-8').splitlines())}
    total = len(rows) * len(g['models']) * len(g['seeds'])
    with open(out, 'a', encoding='utf-8') as fh:
        for model in g['models']:
            for seed in g['seeds']:
                options = {'temperature': g['temperature'], 'seed': seed, 'num_ctx': g['num_ctx'], 'num_predict': g['num_predict']}
                client = Client(OUT / 'generation' / model.replace(':', '_').replace('.', '-'), model,
                                models[model]['digest'], options)
                for task in rows:
                    if (task['task_id'], model, seed) in done:
                        continue
                    # Client.call reads prompts/<template>.txt; the S2 template sits in configs/ instead, so
                    # prompts/ (part of the harness fingerprint) stays unchanged.
                    response = client.call('../configs/s2_natural_prompt', {'prompt': task['prompt']},
                                           unit_id=task['task_id'], purpose='s2_implement', policy='',
                                           test_id=f'{model}/s{seed}', round=0)
                    program = extract(response, task)
                    fh.write(json.dumps({'task_id': task['task_id'], 'model': model, 'seed': seed,
                                         'program': program, 'extracted': program is not None}) + '\n')
                    fh.flush()
                    done.add((task['task_id'], model, seed))
                    write_json(OUT / 'generation_progress.json', {'done': len(done), 'total': total,
                               'percent': round(100 * len(done) / total, 1), 'updated': now()})
                print(f'{model} seed {seed}: {len(done)}/{total}', flush=True)


def check_base(task, program):
    from gbe.execute import execute
    prelude = 'from solution import *\n' + task['test']
    test = f"def test_benchmark():\n    check({task['entry_point']})\n"
    return execute(program, prelude, test, timeout=30)['outcome']


def filter_candidates():
    rows = {t['task_id']: t for t in tasks()}
    raw = [json.loads(l) for l in (OUT / 'candidates_raw.jsonl').read_text(encoding='utf-8').splitlines()]
    out_path = OUT / 'candidates.jsonl'
    done = {}
    if out_path.exists():
        for r in map(json.loads, out_path.read_text(encoding='utf-8').splitlines()):
            done[(r['task_id'], r['model'], r['seed'])] = r
    limit = CONFIG['filter']['time_limit_s']
    with open(out_path, 'a', encoding='utf-8') as fh:
        for i, c in enumerate(raw):
            key = (c['task_id'], c['model'], c['seed'])
            if key in done:
                continue
            task = rows[c['task_id']]
            record = {'task_id': c['task_id'], 'model': c['model'], 'seed': c['seed'], 'status': 'NOT_EXTRACTED'}
            if c['program']:
                base = check_base(task, c['program'])
                record['base'] = base
                if base != 'PASS':
                    record['status'] = 'FAILS_BASE'
                else:
                    result = run_inputs(c['program'], task['entry_point'], all_inputs(task), timeout=limit)
                    if not isinstance(result, list):
                        record['status'] = result  # TIMEOUT or CRASH
                    elif any(s != 'ok' for s, _ in result):
                        record['status'] = 'RAISES'
                        record['errors'] = sum(s != 'ok' for s, _ in result)
                    else:
                        ref = pickle.load(open(EXPECTED / (c['task_id'].replace('/', '_') + '.pkl'), 'rb'))
                        atol = float(task.get('atol') or 0)
                        diffs = [j for j, ((_, v), r) in enumerate(zip(result, ref)) if not same(v, r, atol)]
                        record['n_inputs'], record['n_differ'] = len(ref), len(diffs)
                        record['first_differ'] = diffs[:5]
                        record['status'] = 'FAULT' if diffs else 'CORRECT'
            fh.write(json.dumps(record) + '\n')
            fh.flush()
            if i % 50 == 0:
                print(f'{i + 1}/{len(raw)} filtered', flush=True)


def select():
    order = {m: i for i, m in enumerate(CONFIG['generation']['models'])}
    rows = {t['task_id']: t for t in tasks()}
    raw = {(r['task_id'], r['model'], r['seed']): r for r in
           map(json.loads, (OUT / 'candidates_raw.jsonl').read_text(encoding='utf-8').splitlines())}
    faults = [r for r in map(json.loads, (OUT / 'candidates.jsonl').read_text(encoding='utf-8').splitlines())
              if r['status'] == 'FAULT']
    chosen = {}
    for r in sorted(faults, key=lambda r: (r['n_differ'], order[r['model']], r['seed'])):
        chosen.setdefault(r['task_id'], r)
    pairs = {}
    for tid, r in sorted(chosen.items(), key=lambda kv: int(kv[0].split('/')[-1])):
        task = rows[tid]
        pairs[tid] = {'entry_point': task['entry_point'], 'prompt': task['prompt'], 'author_model': r['model'],
                      'seed': r['seed'], 'n_inputs': r['n_inputs'], 'n_differ': r['n_differ'],
                      'programs': {'buggy': raw[(tid, r['model'], r['seed'])]['program'],
                                   'fixed': task['prompt'] + task['canonical_solution']}}
    target = ROOT / 'data' / 's2' / 'natural_faults.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(pairs, indent=1) + '\n', encoding='utf-8')
    # Pin the file and record two-run sanity evidence for the harness (benchmark HumanEvalPlusNatural). The
    # benchmark test is the HumanEval+ input set: a version passes when it returns the canonical value on
    # every input. HumanEval's own check() cannot serve, because every selected fault passes it.
    from gbe.util import digest
    write_json(ROOT / 'configs' / 'natural.json', {
        'purpose': 'S2 natural LLM faults (scripts/s2_natural_faults.py, configs/s2_natural.json)',
        'file': 'data/s2/natural_faults.json', 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    evidence = {}
    for tid, p in pairs.items():
        task = rows[tid]
        ref = pickle.load(open(EXPECTED / (tid.replace('/', '_') + '.pkl'), 'rb'))
        atol = float(task.get('atol') or 0)
        entry = {}
        for condition in ('fixed', 'buggy'):
            outcomes = []
            for _ in range(2):
                result = run_inputs(p['programs'][condition], p['entry_point'], all_inputs(task),
                                    timeout=CONFIG['filter']['time_limit_s'])
                if not isinstance(result, list):
                    outcomes.append('TIMEOUT')
                else:
                    ok = all(s == 'ok' and same(v, r, atol) for (s, v), r in zip(result, ref))
                    outcomes.append('PASS' if ok else 'FAIL')
            entry[condition] = outcomes
        entry['source_hashes'] = {c: digest(p['programs'][c]) for c in ('fixed', 'buggy')}
        evidence[f"HumanEvalPlusNatural/{tid.split('/')[-1]}"] = entry
    write_json(ROOT / 'configs' / 'natural_sanity.json', evidence)
    from collections import Counter
    usable = sum(e['fixed'] == ['PASS', 'PASS'] and 'PASS' not in e['buggy'] for e in evidence.values())
    print(f'{len(pairs)} tasks with a fault ({usable} usable); by author model: '
          f'{dict(Counter(p["author_model"] for p in pairs.values()))}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=('expected', 'generate', 'filter', 'select'))
    a = ap.parse_args()
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.GetCurrentProcess.restype = ctypes.c_void_p
        kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), BELOW_NORMAL)
    {'expected': expected, 'generate': generate, 'filter': filter_candidates, 'select': select}[a.action]()
