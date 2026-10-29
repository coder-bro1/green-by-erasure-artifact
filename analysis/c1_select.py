"""Stage C (docs/C1_PROTOCOL.md): eligibility steps 1 and 4 for every BugsInPy bug, and the random selection order.

Step 1: the fix patch changes exactly one non-test Python file, and every changed line of the buggy version lies in
the body of one function or method (innermost def in the buggy file's syntax tree; added lines are placed at the
buggy line they follow). The buggy file comes from the GitHub API at the buggy commit (read only, cached by
c2_step3.gh). Step 4: the function plus its module's import lines fit in 6,000 tokens (4 characters per token).
Steps 2 (installation) and 3 (developer test) are checked later per project, in this script's order.

Order: projects shuffled with seed gbe-c1-v1, then the bugs of each project shuffled with the same seed.
Writes runs/c1/selection.json (every bug with its step results and the function) and review/out/c1_attrition.md.
Runs in .venv-c2. Usage: .venv-c2\\Scripts\\python.exe analysis\\c1_select.py
"""
import ast
import base64
import json
import random
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from c2_step3 import gh  # noqa: E402

BIP = ROOT / 'data' / 'c1' / 'BugsInPy' / 'projects'
SEED = 'gbe-c1-v1'
TEST_PATH = re.compile(r'(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_test\.py$|conftest\.py$')


def info(path):
    out = {}
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'(\w+)="(.*)"', line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


def patch_files(text):
    """{path: [buggy line numbers touched]} for every file in a unified diff."""
    files, current, old = {}, None, 0
    for line in text.splitlines():
        if line.startswith('diff --git'):
            current = None
        elif line.startswith('--- '):
            continue
        elif line.startswith('+++ '):
            path = line[4:].strip()
            current = path[2:] if path.startswith('b/') else path
            files.setdefault(current, [])
        elif line.startswith('@@'):
            m = re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@', line)
            old = int(m.group(1)) if m else 0
        elif current is not None:
            if line.startswith('-'):
                files[current].append(old)
                old += 1
            elif line.startswith('+'):
                files[current].append(max(old - 1, 1))
            else:
                old += 1
    return files


def enclosing(tree, line):
    best = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno <= line <= node.end_lineno:
            if best is None or node.lineno >= best.lineno:
                best = node
    return best


def main():
    projects = sorted(p.name for p in BIP.iterdir() if p.is_dir())
    rng = random.Random(SEED)
    rng.shuffle(projects)
    rows = []
    for project in projects:
        pinfo = info(BIP / project / 'project.info')
        repo = pinfo['github_url'].rstrip('/').split('github.com/')[1]
        bugs = sorted((p.name for p in (BIP / project / 'bugs').iterdir() if p.is_dir()), key=int)
        random.Random(f'{SEED}-{project}').shuffle(bugs)
        for rank, bug in enumerate(bugs):
            d = BIP / project / 'bugs' / bug
            binfo = info(d / 'bug.info')
            row = {'project': project, 'bug': int(bug), 'rank_in_project': rank, 'repo': repo,
                   'python_version': binfo.get('python_version'), 'buggy': binfo.get('buggy_commit_id'),
                   'fixed': binfo.get('fixed_commit_id'), 'test_file': binfo.get('test_file'), 'step1': None, 'step4': None}
            files = {f: ls for f, ls in patch_files((d / 'bug_patch.txt').read_text(encoding='utf-8', errors='replace')).items()
                     if f.endswith('.py') and not TEST_PATH.search(f)}
            if len(files) != 1:
                row['step1'] = f'fail: {len(files)} non-test Python files changed'
                rows.append(row)
                continue
            path, lines = next(iter(files.items()))
            data = gh(f'repos/{repo}/contents/{quote(path)}?ref={row["buggy"]}')
            if not isinstance(data, dict) or data.get('encoding') != 'base64':
                row['step1'] = 'fail: buggy file not retrievable'
                rows.append(row)
                continue
            source = base64.b64decode(data['content']).decode('utf-8', 'replace')
            try:
                tree = ast.parse(source)
            except SyntaxError:
                row['step1'] = 'fail: buggy file does not parse with this Python'
                rows.append(row)
                continue
            funcs = {enclosing(tree, n) for n in lines}
            if None in funcs or len(funcs) != 1:
                row['step1'] = f'fail: changes span {len(funcs - {None})} functions' + (' and module-level code' if None in funcs else '')
                rows.append(row)
                continue
            fn = funcs.pop()
            row.update(step1='pass', file=path, function=fn.name, function_lines=[fn.lineno, fn.end_lineno])
            imports = [l for l in source.splitlines() if re.match(r'\s*(import|from)\s', l)]
            body = '\n'.join(source.splitlines()[fn.lineno - 1:fn.end_lineno])
            tokens = (len(body) + len('\n'.join(imports))) / 4
            row['prompt_tokens_est'] = round(tokens)
            row['step4'] = 'pass' if tokens <= 6000 else 'fail: over 6,000 tokens'
            rows.append(row)
        print(project, sum(r['step1'] == 'pass' for r in rows if r['project'] == project), 'of', len(bugs), 'pass step 1', flush=True)
    out = ROOT / 'runs' / 'c1'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'selection.json').write_text(json.dumps({'seed': SEED, 'project_order': projects, 'bugs': rows}, indent=1),
                                        encoding='utf-8')
    lines = ['# C1 attrition, steps 1 and 4', '', 'Computed by `analysis/c1_select.py`; project order (seed gbe-c1-v1): '
             + ', '.join(projects) + '.', '', '| Project | Bugs | Step 1: one function in one file | Step 4: prompt fits |', '|---|---:|---:|---:|']
    for project in projects:
        rs = [r for r in rows if r['project'] == project]
        lines.append(f"| {project} | {len(rs)} | {sum(r['step1'] == 'pass' for r in rs)} | {sum(r['step4'] == 'pass' for r in rs)} |")
    lines.append(f"| all | {len(rows)} | {sum(r['step1'] == 'pass' for r in rows)} | {sum(r['step4'] == 'pass' for r in rows)} |")
    (ROOT / 'review' / 'out' / 'c1_attrition.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
