"""For each QuixBugs program: extract the trailing description block from the buggy file and run its
>>> examples against the correct and the buggy program. Usage: python -I check_desc.py <QuixBugs dir>"""
import ast, json, re, subprocess, sys
from pathlib import Path
Q = Path(sys.argv[1])
res = {}
for f in sorted((Q / 'python_programs').glob('*.py')):
    if f.stem.endswith('_test') or f.stem == 'node':
        continue
    src = f.read_text(encoding='utf-8')
    tree = ast.parse(src)
    docs = [n.value.value for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)]
    desc = docs[-1] if docs else ''
    ex = re.findall(r'>>> (.+)\n\s*(.+)', desc)
    row = {'has_desc': bool(desc), 'has_io': 'Input' in desc and 'Output' in desc, 'examples': len(ex)}
    for version, folder in (('correct', 'correct_python_programs'), ('buggy', 'python_programs')):
        ok = 0
        for call, want in ex:
            code = f"import sys; sys.path[:0]=[{str(Q/folder)!r},{str(Q/'python_programs')!r}]\nfrom {f.stem} import *\nprint(repr({call}) == repr({want}) or {call} == {want})"
            try:
                p = subprocess.run([sys.executable, '-I', '-c', code], capture_output=True, text=True, timeout=5)
                ok += p.stdout.strip() == 'True'
            except subprocess.TimeoutExpired:
                pass
        row[version + '_examples_pass'] = ok
    res[f.stem] = row
print(json.dumps(res, indent=0))
