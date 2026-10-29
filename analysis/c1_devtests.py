"""C1 protocol section 10: lift the developers' bug-revealing tests into the harness and seed run c1_devtests_qwen25.

For every eligible bug, each pytest test of its run_test.sh is lifted (section 10, item 2) from the buggy checkout's
test file (the developer's test files are the fixed commit's in both checkouts). A lifted test is kept when it fails
on the buggy and passes on the fixed version, twice each, in the bug's environment with the exact prelude used.
Kept tests become the suite of both units of their bug: runs/c1_devtests_qwen25/units/<unit>/generated.json, which
the runner then uses instead of generating. Writes configs/c1_devtests_subset.json and review/out/c1_devtests_lift.md.
Usage: .venv\\Scripts\\python.exe analysis\\c1_devtests.py
"""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.execute import execute  # noqa: E402
from gbe.util import write_json  # noqa: E402

W = Path(r'<work>')
BIP = ROOT / 'data' / 'c1' / 'BugsInPy' / 'projects'
RUN = 'c1_devtests_qwen25'
SLUG = 'qwen2-5-coder-7b-instruct'


def defined_names(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return {n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)}
    return set()


def used_names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)} | \
           {n.value.id for n in ast.walk(node) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}


def lift(src, names, package, test_dir):
    """(prelude, source, test name) or (None, reason)."""
    tree = ast.parse(src)
    if len(names) == 1:
        target = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == names[0]), None)
    else:
        cls = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == names[0]), None)
        if cls is None:
            return None, 'class not found'
        if cls.bases:
            return None, f'class has base classes ({", ".join(ast.unparse(b) for b in cls.bases)})'
        target = next((n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == names[1]), None)
        if target is not None:
            if any(isinstance(n, ast.Name) and n.id == 'self' for n in ast.walk(target)):
                return None, 'method uses self'
            target.args.args = [a for a in target.args.args if a.arg != 'self']
    if target is None:
        return None, 'test not found'
    params = [a.arg for a in target.args.args]
    has_param_marks = any('parametrize' in ast.unparse(d) for d in target.decorator_list)
    if params and not has_param_marks:
        return None, f'uses fixtures ({", ".join(params)})'
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    others = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))
              and not (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test'))
              and not (isinstance(n, ast.ClassDef) and n.name.startswith('Test'))]
    needed, frontier = [], used_names(target)
    for _ in range(2):  # names the test uses, followed once
        new = [n for n in others if n not in needed and defined_names(n) & frontier]
        needed += new
        frontier = set().union(*[used_names(n) for n in new]) if new else set()
    needed.sort(key=lambda n: n.lineno)
    sibling = any(isinstance(n, ast.ImportFrom) and n.level == 0 and n.module and n.module.split('.')[0] in ('utils', 'fixtures', 'conftest')
                  or isinstance(n, ast.ImportFrom) and n.level > 0 for n in imports)
    lines = ['from solution import *']
    if sibling:
        lines += ['import os, sys, ' + package,
                  f"sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname({package}.__file__)), {test_dir!r}))"]
    for n in imports:
        if isinstance(n, ast.ImportFrom) and n.level > 0:
            n = ast.ImportFrom(module=n.module, names=n.names, level=0)
        lines.append(ast.unparse(n))
    lines += [ast.unparse(n) for n in needed]
    return ('\n'.join(lines) + '\n', ast.unparse(target), target.name), None


def main():
    tasks = json.loads((ROOT / 'data' / 'c1' / 'tasks.json').read_text(encoding='utf-8'))
    report = ['# C1 section 10: developers\' tests lifted into the harness', '',
              'Computed by `analysis/c1_devtests.py`. Kept: fails on buggy and passes on fixed, twice each.', '',
              '| Bug | Test | Result | Buggy | Fixed |', '|---|---|---|---|---|']
    kept_bugs = {}
    for tid, t in tasks.items():
        bug = tid.split('/')[1]
        cmds = [l.strip() for l in (BIP / t['project'] / 'bugs' / str(t['bug']) / 'run_test.sh').read_text(
            encoding='utf-8', errors='replace').splitlines() if l.strip()]
        for c in cmds:
            if c.startswith('python -m unittest'):
                report.append(f'| {bug} | {c.split()[-1][-60:]} | not lifted: unittest | | |')
                continue
            node = c.split()[-1]
            parts = node.split('::')
            file, names = parts[0], parts[1:]
            src = (W / 'work' / bug / 'buggy' / file).read_text(encoding='utf-8')
            lifted, reason = lift(src, names, t['module'].split('.')[0], Path(file).parent.as_posix())
            if lifted is None:
                report.append(f'| {bug} | {"::".join(names)} | not lifted: {reason} | | |')
                continue
            prelude, source, name = lifted
            if len(names) == 2 and any(x['name'] == name for x in kept_bugs.get(tid, [])):
                # Same method name in two classes (pandas-23): the lifted function takes the class name as suffix.
                new = f'{name}_{names[0]}'
                source = source.replace(f'def {name}(', f'def {new}(', 1)
                name = new
            outs = {}
            for v in ('buggy', 'fixed'):
                outs[v] = [execute('', prelude, source, runtime=dict(t['runtime'][v], timeout=30))['outcome'] for _ in range(2)]
            ok = all(o != 'PASS' for o in outs['buggy']) and all(o == 'PASS' for o in outs['fixed']) \
                and not any(o in ('COLLECT_ERROR', 'TIMEOUT') for o in outs['buggy'])
            report.append(f"| {bug} | {'::'.join(names)} | {'kept' if ok else 'not kept'} | {', '.join(outs['buggy'])} | {', '.join(outs['fixed'])} |")
            print(bug, name, outs, 'KEPT' if ok else '', flush=True)
            if ok:
                kept_bugs.setdefault(tid, []).append({'name': name, 'source': source, 'prelude': prelude})
    run_dir = ROOT / 'runs' / RUN
    for tid, tests in kept_bugs.items():
        # One suite per bug; tests that need different preludes keep their own (the policies carry a prelude per test).
        names = [x['name'] for x in tests]
        assert len(set(names)) == len(names), names
        prelude = tests[0]['prelude'] if all(x['prelude'] == tests[0]['prelude'] for x in tests) else None
        if prelude is None:
            merged = []
            for x in tests:
                for line in x['prelude'].splitlines():
                    if line not in merged:
                        merged.append(line)
            prelude = '\n'.join(merged) + '\n'
        bug = tid.split('/')[1]
        for cond in ('buggy', 'fixed'):
            uid = f'BugsInPy-{bug}__{cond}__{SLUG}__s0__code'
            suite = {'prelude': prelude, 'tests': [{'name': x['name'], 'source': x['source']} for x in tests],
                     'parse_status': 'OK', 'raw_response': '(developer tests, C1 protocol section 10)',
                     'responses': [], 'origin': 'developer'}
            write_json(run_dir / 'units' / uid / 'generated.json', suite)
    write_json(ROOT / 'configs' / 'c1_devtests_subset.json', {'pairs': sorted(kept_bugs)})
    report += ['', f'Kept: {sum(len(v) for v in kept_bugs.values())} tests in {len(kept_bugs)} bugs.']
    (ROOT / 'review' / 'out' / 'c1_devtests_lift.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    print(report[-1])


if __name__ == '__main__':
    main()
