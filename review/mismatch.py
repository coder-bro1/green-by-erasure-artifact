import sys; sys.path.insert(0,'review'); import check_phase1 as c, json, pathlib, subprocess, tempfile
data=c.load_dataset(); u='HumanEvalFix-37__fixed__qwen2-5-coder-7b-instruct__s0__spec'
g=json.loads(pathlib.Path('runs/phase1_pilot/units',u,'policy_P1.json').read_text(encoding='utf-8'))
t=next(t for t in g['tests'] if t['test_id'].endswith('/t9')); print(t['source'][:400])
row=data['Python/37']
for v in ('fixed','buggy'):
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d,'solution.py').write_text(c.program(row,v),encoding='utf-8'); pathlib.Path(d,'test_r.py').write_text(t['prelude']+'\n'+t['source'],encoding='utf-8')
        import time; s=time.time(); p=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_r.py'],cwd=d,capture_output=True,text=True,timeout=60); print(v,p.returncode,round(time.time()-s,1),'s')
