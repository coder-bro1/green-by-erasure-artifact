import json, ast, csv, collections, pathlib, sys
sys.path.insert(0,'review'); import check_phase1 as c
data=c.load_dataset()
rows={(r['test_id'],r['stage']):r for r in csv.DictReader(open('runs/phase1_pilot/tests.csv',encoding='utf-8'))}
cnt=collections.Counter(); ex=[]
for u in pathlib.Path('runs/phase1_pilot/units').iterdir():
    pair=next(r['pair_id'] for (t,s),r in rows.items() if t.startswith(u.name+'/'))
    ep=data[pair]['entry_point']
    for pol in ('P2','P3','P4'):
        for t in json.loads((u/f'policy_{pol}.json').read_text(encoding='utf-8'))['tests']:
            try: tree=ast.parse(t['prelude']+'\n'+t['source'])
            except SyntaxError: continue
            shadow=any(isinstance(n,(ast.FunctionDef,ast.Lambda)) and getattr(n,'name','')==ep for n in ast.walk(tree)) or any(isinstance(n,ast.Assign) and any(getattr(tg,'id','')==ep for tg in n.targets) for n in ast.walk(tree))
            if shadow:
                r=rows.get((t['test_id'],pol),{})
                cnt[(pol,t['final_status'],r.get('condition'),r.get('label'))]+=1
                if len(ex)<3: ex.append(t['test_id'])
print(dict(cnt)); print(ex)
