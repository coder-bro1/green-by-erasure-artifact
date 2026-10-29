"""D11 agents: the final suites under plain pytest (stage A-6 of docs/PHASE2_REVISION_PLAN.md, review item R3).

scripts/d11_evaluate.py runs every final suite with --runxfail, so a test the agent marked xfail is judged by its
own assertion (diagnostic evaluation). A developer's CI runs plain pytest: an xfail-marked test that fails is an
expected failure and does not turn the suite red, and a strict xfail test fails once the bug is fixed. This script
runs the same final suites, unchanged, against the original fixed and buggy programs with plain pytest and reports
per suite:
- reveals (diagnostic): from evaluation.json, a test passes on the fixed and fails on the buggy program under
  --runxfail;
- active evidence: under plain pytest a test fails on the buggy program and passes on the fixed one;
- encodes: from evaluation.json, a test passes on the buggy and fails on the fixed program;
- CI separates the versions: under plain pytest the suite is red on the buggy program and green on the fixed one.
Each version runs once (the diagnostic evaluation already ran every case twice for flakiness). Below-normal
priority, 4 workers. Writes runs/d11/<setting>/evaluation_plain.json and review/out/d11_plain.md.
Usage: python analysis/d11_plain.py
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'src'))
SETTINGS = ['gpt-6.1-sol_medium_frozen', 'gpt-6.1-sol_medium_frozen_disguised', 'gpt-6.1-sol_medium_frozen_quixbugs',
            'gpt-6-luna_high_frozen', 'claude-opus-5-5_medium_frozen', 'claude-opus-5-5_medium_frozen_disguised',
            'claude-opus-5-5_medium_frozen_quixbugs', 'gpt-6.1-sol_medium_report', 'gpt-6.1-sol_medium_report_quixbugs',
            'gpt-6-luna_high_report', 'claude-opus-5-5_medium_report']
_ROWS = None


def plain_run(test_files, solution, support):
    """{case: PASS|FAIL|SKIP|TIMEOUT} under plain pytest (xfailed and skipped cases are SKIP; a strict XPASS fails)."""
    import d11_evaluate as ev
    with ev.private_tmp() as d:
        for f in test_files:
            (Path(d) / f.name).write_bytes(f.read_bytes())
        Path(d, 'solution.py').write_text(solution, encoding='utf-8')
        for name, text in (support or {}).items():
            if not (Path(d) / name).exists():
                Path(d, name).write_text(text, encoding='utf-8')
        env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1')
        try:
            subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--rootdir=.', '--junitxml=r.xml',
                            *[f.name for f in test_files]], cwd=d, env=env, capture_output=True, timeout=300)
        except subprocess.TimeoutExpired:
            return {'__suite__': 'TIMEOUT'}
        out = {}
        if (Path(d) / 'r.xml').exists():
            for case in ET.parse(Path(d) / 'r.xml').iter('testcase'):
                key = case.get('classname', '').split('.')[-1] + '::' + case.get('name', '')
                failed = any(c.tag in ('failure', 'error') for c in case)
                skipped = any(c.tag == 'skipped' for c in case)
                out[key] = 'FAIL' if failed else ('SKIP' if skipped else 'PASS')
        return out


def plain_task(task_dir):
    global _ROWS
    import d11_evaluate as ev
    if _ROWS is None:
        _ROWS = {r['task_id']: r for r in ev.download()[0]}
    task_dir = Path(task_dir)
    attempt = sorted(task_dir.glob('attempt*'))[-1]
    result = json.loads((attempt / 'result.json').read_text(encoding='utf-8'))
    task = result['task']
    final = attempt / 'final'
    tests = sorted(p for p in final.glob('*.py') if p.name != 'solution.py')
    versions, support, _ = ev.originals(task, _ROWS)
    outcomes = {c: plain_run(tests, versions[c], support) for c in versions} if tests else {c: {} for c in versions}
    cases = set().union(*[set(o) for o in outcomes.values()]) - {'__suite__'}
    get = lambda c, k: outcomes[c].get(k, 'MISSING')
    active = any(get('buggy', k) == 'FAIL' and get('fixed', k) == 'PASS' for k in cases)
    red_buggy = any(v in ('FAIL', 'TIMEOUT') for v in outcomes['buggy'].values())
    red_fixed = any(v in ('FAIL', 'TIMEOUT') for v in outcomes['fixed'].values())
    return {'task': task_dir.name, 'order': task.get('order'), 'pair_id': task.get('pair_id') or task.get('task_id'), 'condition': task.get('condition'),
            'cases': len(cases), 'active_reveals': active, 'red_on_buggy': red_buggy, 'red_on_fixed': red_fixed,
            'skipped_on_buggy': sum(v == 'SKIP' for v in outcomes['buggy'].values())}


def main():
    if os.name == 'nt':
        import ctypes
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        k.SetPriorityClass(k.GetCurrentProcess(), 0x4000)
    lines = ['# D11: final suites under plain pytest against the diagnostic evaluation', '',
             'Computed by `analysis/d11_plain.py`. Reveals (diagnostic) and encodes come from `evaluation.json` (`--runxfail`);',
             'active evidence and the CI columns from running the same final suites with plain pytest. CI separates the',
             'versions: the suite is red on the buggy program and green on the fixed one.', '',
             '| Setting | Condition | Tasks | Reveals (diagnostic) | Active evidence (plain pytest) | Encodes the bug | Encodes, reveals nothing | Red on buggy | CI separates the versions |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for setting in SETTINGS:
        base = ROOT / 'runs' / 'd11' / setting
        if not (base / 'evaluation.json').exists():
            continue
        diag = {r['order']: r for r in json.loads((base / 'evaluation.json').read_text(encoding='utf-8'))}
        task_dirs = sorted(p for p in base.iterdir() if p.is_dir())
        out_path = base / 'evaluation_plain.json'
        if out_path.exists():
            plain = json.loads(out_path.read_text(encoding='utf-8'))
        else:
            with ProcessPoolExecutor(max_workers=4) as pool:
                plain = list(pool.map(plain_task, [str(d) for d in task_dirs]))
            out_path.write_text(json.dumps(plain, indent=1), encoding='utf-8')
        by_order = {}
        for p in plain:
            order = p['order']
            by_order[order] = p
        for cond in ('buggy', 'fixed'):
            orders = [o for o, r in diag.items() if r['condition'] == cond]
            if not orders:
                continue
            n = len(orders)
            rev = sum(diag[o]['suite_reveals_bug'] for o in orders)
            act = sum(by_order[o]['active_reveals'] for o in orders if o in by_order)
            enc = sum(diag[o]['suite_encodes_bug'] for o in orders)
            lock = sum(diag[o]['suite_encodes_bug'] and not diag[o]['suite_reveals_bug'] for o in orders)
            red = sum(by_order[o]['red_on_buggy'] for o in orders if o in by_order)
            sep = sum(by_order[o]['red_on_buggy'] and not by_order[o]['red_on_fixed'] for o in orders if o in by_order)
            lines.append(f'| {setting} | {cond} | {n} | {rev} | {act} | {enc} | {lock} | {red} | {sep} |')
        print(setting, 'done', flush=True)
    (ROOT / 'review' / 'out' / 'd11_plain.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
