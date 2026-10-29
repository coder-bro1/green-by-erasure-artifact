"""Stage C (docs/C1_PROTOCOL.md sections 5 and 6): pipeline inputs for the 30 eligible bugs.

For every eligible bug (runs/c1/install/*.json, step 3 passed):
- program (per version): the module's import lines, the headers of the enclosing classes (if the changed
  function is a method), and the changed function, read from the buggy and fixed checkouts in <work>.
- entry_point: the top-level name a test imports (the function, or its outermost class); module: its dotted path.
- requirement for the judge (section 5): the function's signature and docstring in the buggy version plus the
  first line of the fix commit's message, with code spans removed; written to data/c1/specs/<bug>.txt.
- runtime (per version): the environment's Python, PYTHONPATH (bug.info entries and the checkout root), the
  checkout root as the program-under-test root, and the per-test time limit: 5 s as in Phase 2, or 30 s when
  the start-up of one trivial test in that environment exceeds 2.5 s (section 6).
Writes data/c1/tasks.json, configs/c1.json (pin: sha256 and BugsInPy commit) and configs/c1_sanity.json (the
developer-test outcomes of step 3 bound to the program hashes, read by gbe.runner like the other benchmarks).
Runs in .venv. Usage: .venv\\Scripts\\python.exe analysis\\c1_build_tasks.py
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.execute import execute  # noqa: E402
from gbe.util import digest, write_json  # noqa: E402

W = Path(r'<work>')
BIP = ROOT / 'data' / 'c1' / 'BugsInPy'
BENCHMARK = 'BugsInPy'


def info(path):
    out = {}
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'\s*(\w+)\s*=\s*"(.*)"', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def chain_at(tree, line):
    """Enclosing class/def nodes, outermost first, of the innermost def spanning the line."""
    best = None
    def walk(node, path):
        nonlocal best
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and \
                    child.lineno <= line <= child.end_lineno:
                here = path + [child]
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    best = here
                walk(child, here)
    walk(tree, [])
    return best


def find_chain(tree, names):
    """The same chain of names in another version of the file."""
    nodes, body = [], tree.body
    for name in names:
        node = next((n for n in body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                     and n.name == name), None)
        if node is None:
            return None
        nodes.append(node)
        body = node.body
    return nodes


def header(source_lines, node):
    """The class or def line(s) up to the colon, with decorators."""
    start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
    return '\n'.join(source_lines[start:node.body[0].lineno - 1])


def program_text(source, chain):
    lines = source.splitlines()
    imports = [l for l in lines if re.match(r'(import|from)\s', l)]
    parts = ['\n'.join(imports), '']
    for outer in chain[:-1]:
        parts.append(header(lines, outer))
        indent = ' ' * (outer.body[0].col_offset)
        parts.append(indent + '...')
    fn = chain[-1]
    start = (fn.decorator_list[0].lineno if fn.decorator_list else fn.lineno) - 1
    parts.append('\n'.join(lines[start:fn.end_lineno]))
    return '\n'.join(parts).strip('\n') + '\n'


def requirement(source, fn, commit_line):
    lines = source.splitlines()
    # The def line(s) only: comments and blank lines before the first statement are not part of it.
    signature = '\n'.join(l for l in lines[fn.lineno - 1:fn.body[0].lineno - 1]
                          if l.strip() and not l.strip().startswith('#')).strip()
    doc = ast.get_docstring(fn, clean=True) or ''
    message = re.sub(r'`[^`]*`', '', commit_line).strip()
    message = re.sub(r'\s{2,}', ' ', message)
    text = signature + ('\n' + doc if doc else '') + '\n\nThe fix to this function is described as: ' + message
    return text.strip() + '\n'


def module_name(path):
    parts = list(Path(path).with_suffix('').parts)
    if parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join(parts)


def runtime(bug_dir, version, binfo):
    wt = bug_dir / version
    pp = []
    for p in (p.strip().strip('/') for p in binfo.get('pythonpath', '').split(';') if p.strip()):
        parts = Path(p).parts
        if len(parts) > 1:
            pp.append(str(wt.joinpath(*parts[1:])))
    return {'python': str(bug_dir / f'env-{version}' / 'Scripts' / 'python.exe'), 'pythonpath': pp + [str(wt)],
            'put_roots': [str(wt)], 'work_root': str(W / 'exec')}


def startup_seconds(rt, module, entry):
    shim = f'from {module} import *\nfrom {module} import {entry}\n'
    rt = dict(rt, shim=shim, timeout=60)
    best = None
    for _ in range(2):
        t0 = time.monotonic()
        out = execute('', 'from solution import *\n', 'def test_startup():\n    assert True\n', runtime=rt)
        took = time.monotonic() - t0
        if out['outcome'] != 'PASS':
            raise RuntimeError(f'start-up test did not pass: {out.get("output", "")[-800:]}')
        best = took if best is None else min(best, took)
    return best


def main():
    sel = {(b['project'], b['bug']): b for b in json.loads((ROOT / 'runs' / 'c1' / 'selection.json').read_text(encoding='utf-8'))['bugs']}
    tasks, sanity = {}, {}
    (ROOT / 'data' / 'c1' / 'specs').mkdir(parents=True, exist_ok=True)
    for f in sorted((ROOT / 'runs' / 'c1' / 'install').glob('*.json')):
        r = json.loads(f.read_text(encoding='utf-8'))
        if r.get('step3') != 'pass':
            continue
        project, bug = r['project'], r['bug']
        bug_id = f'{project}-{bug}'
        b = sel[(project, bug)]
        binfo = info(BIP / 'projects' / project / 'bugs' / str(bug) / 'bug.info')
        bug_dir = W / 'work' / bug_id
        sources = {v: (bug_dir / v / b['file']).read_text(encoding='utf-8') for v in ('buggy', 'fixed')}
        tree = ast.parse(sources['buggy'])
        chain = chain_at(tree, b['function_lines'][0])
        assert chain and chain[-1].name == b['function'], (bug_id, [n.name for n in chain or []])
        names = [n.name for n in chain]
        fixed_chain = find_chain(ast.parse(sources['fixed']), names)
        assert fixed_chain, (bug_id, 'function missing in fixed version')
        nested = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in chain[:-1])
        module = module_name(b['file'])
        entry = names[0]
        commit = subprocess.run(['git', '-C', str(W / 'repos' / project), 'log', '-1', '--format=%s', binfo['fixed_commit_id']],
                                capture_output=True, text=True, encoding='utf-8').stdout.strip()
        spec = requirement(sources['buggy'], chain[-1], commit)
        (ROOT / 'data' / 'c1' / 'specs' / f'{bug_id}.txt').write_text(spec, encoding='utf-8')
        programs = {'buggy': program_text(sources['buggy'], chain), 'fixed': program_text(sources['fixed'], fixed_chain)}
        assert programs['buggy'] != programs['fixed'], (bug_id, 'the shown function is identical in both versions')
        rts = {}
        for v in ('buggy', 'fixed'):
            rt = runtime(bug_dir, v, binfo)
            rt['shim'] = f'from {module} import *\nfrom {module} import {entry}\n'
            s = startup_seconds(rt, module, entry)
            rt['startup_s'] = round(s, 2)
            rts[v] = rt
        limit = 30 if max(rt['startup_s'] for rt in rts.values()) > 2.5 else 5
        for rt in rts.values():
            rt['timeout'] = limit
        task_id = f'{BENCHMARK}/{bug_id}'
        tasks[task_id] = {'task_id': task_id, 'benchmark': BENCHMARK, 'project': project, 'bug': bug,
                          'entry_point': entry, 'function': b['function'], 'qualname': '.'.join(names),
                          'nested_in_function': nested, 'module': module, 'file': b['file'],
                          'programs': programs, 'prompt': spec, 'runtime': rts, 'support': {}, 'bug_type': '',
                          'fix_commit_subject': commit, 'buggy_commit': binfo['buggy_commit_id'],
                          'fixed_commit': binfo['fixed_commit_id']}
        runs = r['runs']
        sanity[task_id] = {'fixed': ['PASS' if x['outcome'] == 'pass' else x['outcome'] for x in runs if x['version'] == 'fixed'],
                           'buggy': ['FAIL' if x['outcome'] == 'fail' else x['outcome'] for x in runs if x['version'] == 'buggy'],
                           'source_hashes': {c: digest(programs[c]) for c in ('fixed', 'buggy')},
                           'evidence': f'runs/c1/install/{bug_id}.json (developer test, two runs per version)'}
        print(f"{bug_id}: entry {entry} ({'.'.join(names)}), module {module}, start-up "
              f"{rts['buggy']['startup_s']}/{rts['fixed']['startup_s']} s, limit {limit} s"
              + (', NESTED' if nested else ''), flush=True)
    out = ROOT / 'data' / 'c1' / 'tasks.json'
    out.write_text(json.dumps(tasks, indent=1), encoding='utf-8')
    bip_commit = subprocess.run(['git', '-C', str(BIP), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    from gbe.c1 import content_hash  # the pin covers the task content, not this machine's runtime paths
    write_json(ROOT / 'configs' / 'c1.json', {'file': 'data/c1/tasks.json', 'sha256': content_hash(tasks),
                                              'bugsinpy_commit': bip_commit, 'tasks': len(tasks)})
    write_json(ROOT / 'configs' / 'c1_sanity.json', sanity)
    print(f'{len(tasks)} tasks written to {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
