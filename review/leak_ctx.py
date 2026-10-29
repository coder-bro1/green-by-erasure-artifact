import json, sys; sys.path.insert(0,'review'); import check_phase1 as c
s='return [x for x in strings if x.startswith(prefix)]'
for l in open('runs/phase1_pilot/llm_calls.jsonl',encoding='utf-8'):
    x=json.loads(l)
    if x.get('unit_id')=='HumanEvalFix-29__buggy__qwen2-5-coder-7b-instruct__s0__spec' and x['purpose']=='free_repair':
        p=c.text_of(x['prompt'])
        if s in p:
            i=p.find(s); print('round',x.get('round'),'test',x.get('test_id')); print(p[max(0,i-900):i+200]); print('======'); break
d=c.load_dataset()['Python/29']; print('BUGGY:',d['buggy_solution']); print('CANON:',d['canonical_solution'])
