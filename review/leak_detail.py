import json, collections, sys
sys.path.insert(0,'review'); import check_phase1 as c
data=c.load_dataset()
rows=list(__import__('csv').DictReader(open('runs/phase1_pilot/tests.csv',encoding='utf-8')))
meta={r['unit_id']:(r['pair_id'],r['condition']) for r in rows}
calls=[json.loads(l) for l in open('runs/phase1_pilot/llm_calls.jsonl',encoding='utf-8')]
units={}
import pathlib
for u in pathlib.Path('runs/phase1_pilot/units').iterdir():
    units[u.name]=json.loads((u/'generated.json').read_text(encoding='utf-8'))
by=collections.Counter(); real=[]
for x in calls:
    if x.get('unit_id') not in meta: continue
    pair,cond=meta[x['unit_id']]; row=data[pair]; prompt=c.text_of(x.get('prompt'))
    allowed=row['prompt']+c.program(row,cond)
    hidden=row['test']+'\n'+(row.get('example_test') or '')+'\n'+(row['canonical_solution'] if cond=='buggy' else row['buggy_solution'])
    gen_text='\n'.join(t['source'] for t in units[x['unit_id']]['tests'])+'\n'+units[x['unit_id']]['raw_response'] if isinstance(units[x['unit_id']].get('raw_response'),str) else '\n'.join(t['source'] for t in units[x['unit_id']]['tests'])
    for line in hidden.splitlines():
        s=line.strip()
        if len(s)>=25 and s not in allowed and s in prompt:
            src='model_generated' if s in gen_text else 'NOT_from_generation'
            by[(x['purpose'],src)]+=1
            if src!='model_generated' or x['purpose']=='generate': real.append((x['purpose'],x['unit_id'],s))
print(dict(by)); print('suspicious:',len(real)); print(real[:6])
