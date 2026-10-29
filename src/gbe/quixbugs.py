"""QuixBugs (Python) as paired tasks, with the benchmark authors' problem description as specification.

Each buggy program in `python_programs/` ends with a description string written by the QuixBugs
authors; the corrected programs do not contain it. Both versions are normalised the same way: bare
string statements are dropped, the description becomes the entry function's docstring, and the module
is re-rendered with `ast.unparse`, so the two versions differ only in the defect. Benchmark tests
(`python_testcases/`, `json_testcases/`, `python_programs/*_test.py`) are read only by `sanity`, never
by the pipeline view.
"""
import ast
import hashlib
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from .util import ROOT, read_json

SOURCE = ROOT / 'data' / 'raw' / 'quixbugs_src' / 'QuixBugs'
NODE_USERS = ('breadth_first_search', 'depth_first_search', 'detect_cycle', 'reverse_linked_list',
              'shortest_path_length', 'topological_ordering')


def description(source):
    tree = ast.parse(source)
    strings = [n.value.value for n in tree.body
               if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)]
    if not strings:
        raise ValueError('No description string')
    return strings[-1].strip('\n')


def normalise(source, entry_point, docstring):
    tree = ast.parse(source)
    tree.body = [n for n in tree.body
                 if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))]
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == entry_point]
    if len(functions) != 1:
        raise ValueError(f'Expected one definition of {entry_point}')
    function = functions[0]
    if function.body and isinstance(function.body[0], ast.Expr) and isinstance(function.body[0].value, ast.Constant):
        function.body = function.body[1:]
    # Indent continuation lines like a hand-written docstring; the text itself is unchanged.
    text = '\n'.join(('    ' + line) if line.strip() and i else line for i, line in enumerate(docstring.splitlines()))
    function.body.insert(0, ast.Expr(ast.Constant(text + '\n    ')))
    return ast.unparse(ast.fix_missing_locations(tree)) + '\n'


def signature_spec(fixed_program, entry_point):
    """Signature plus docstring of the entry function, with the module's imports (like HumanEval's prompt)."""
    tree = ast.parse(fixed_program)
    imports = [ast.unparse(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == entry_point)
    stub = ast.FunctionDef(name=function.name, args=function.args, body=[function.body[0]],
                           decorator_list=[], returns=function.returns, type_params=[])
    return '\n'.join(imports + [ast.unparse(ast.fix_missing_locations(ast.Module([stub], [])))]) + '\n'


def file_hashes():
    return {str(p.relative_to(SOURCE)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
            for folder in ('python_programs', 'correct_python_programs', 'python_testcases', 'json_testcases')
            for p in sorted((SOURCE / folder).glob('*')) if p.is_file()}


def load():
    """Return QuixBugs tasks after checking every source file against configs/quixbugs.json."""
    pinned = read_json(ROOT / 'configs' / 'quixbugs.json')
    if file_hashes() != pinned['file_sha256']:
        raise ValueError('QuixBugs files differ from the pinned commit')
    node = (SOURCE / 'python_programs' / 'node.py').read_text(encoding='utf-8')
    tasks = []
    for path in sorted((SOURCE / 'python_programs').glob('*.py')):
        name = path.stem
        if name.endswith('_test') or name == 'node':
            continue
        buggy_source = path.read_text(encoding='utf-8')
        doc = description(buggy_source)
        programs = {'buggy': normalise(buggy_source, name, doc),
                    'fixed': normalise((SOURCE / 'correct_python_programs' / path.name).read_text(encoding='utf-8'), name, doc)}
        support = {'node.py': node} if name in NODE_USERS else {}
        tasks.append({'task_id': f'QuixBugs/{name}', 'benchmark': 'QuixBugs', 'entry_point': name,
                      'programs': programs, 'prompt': signature_spec(programs['fixed'], name),
                      'support': support, 'bug_type': ''})
    return tasks


def sanity(task, condition, timeout=60):
    """Run the benchmark's own pytest cases on one normalised version. Returns PASS, FAIL or TIMEOUT."""
    name = task['entry_point']
    folder = ROOT / '.scratch' / 'quixbugs_sanity' / uuid.uuid4().hex
    (folder / 'python_programs').mkdir(parents=True)
    (folder / 'python_testcases').mkdir()
    shutil.copytree(SOURCE / 'json_testcases', folder / 'json_testcases')
    shutil.copy(SOURCE / 'conftest.py', folder / 'conftest.py')
    for helper in ('load_testdata.py', 'node.py'):
        if (SOURCE / 'python_testcases' / helper).exists():
            shutil.copy(SOURCE / 'python_testcases' / helper, folder / 'python_testcases' / helper)
    shutil.copy(SOURCE / 'python_programs' / 'node.py', folder / 'python_programs' / 'node.py')
    (folder / 'python_programs' / f'{name}.py').write_text(task['programs'][condition], encoding='utf-8')
    shutil.copy(SOURCE / 'python_testcases' / f'test_{name}.py', folder / 'python_testcases' / f'test_{name}.py')
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1',
               PYTHONPATH=str(folder / 'python_testcases') + os.pathsep + str(folder))
    command = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--rootdir=.', f'python_testcases/test_{name}.py']
    process = subprocess.Popen(command, cwd=folder, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding='utf-8', errors='replace')
    try:
        stdout, _ = process.communicate(timeout=timeout)
        result = 'PASS' if process.returncode == 0 else 'FAIL'
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True) if os.name == 'nt' else process.kill()
        process.communicate()
        result, stdout = 'TIMEOUT', ''
    shutil.rmtree(folder, ignore_errors=True)
    return result, stdout[-400:]
