"""Classify leakage hits for any run: is each flagged line something the model itself wrote earlier
in the same unit (shown back in repair or judge prompts), or material it never produced?

Uses the reviewer's own benchmark rows (review/check_run.py load_dataset: HumanEvalFix from the parquet
file, QuixBugs from the raw files). Spacing is ignored when matching model output, because the harness
re-renders tests with ast.unparse before showing them again (for example `i-1` becomes `i - 1`,
and double quotes become single quotes).
Usage: python review/leak_r2.py <run>"""
import collections, csv, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'review'))
from check_run import load_dataset  # noqa: E402

run = ROOT / 'runs' / sys.argv[1]
data = load_dataset()
rows = list(csv.DictReader(open(run / 'tests.csv', encoding='utf-8')))
meta = {r['unit_id']: (r['pair_id'], r['condition']) for r in rows}
squash = lambda s: re.sub(r'\s+', '', s).replace('"', "'")  # ast.unparse also normalises quotes
seen = collections.defaultdict(str)   # model output so far, per unit (spacing removed)
kinds = collections.Counter(); examples = []
for line in open(run / 'llm_calls.jsonl', encoding='utf-8'):
    c = json.loads(line)
    u = c.get('unit_id')
    if u in meta:
        pair, cond = meta[u]; row = data[pair]
        prompt = c['prompt']
        allowed = row['prompt'] + row[cond] + ''.join(row['support'].values())
        hidden = row['hidden_tests'] + '\n' + row['bodies']['fixed' if cond == 'buggy' else 'buggy']
        lines = [s for s in (l.strip() for l in hidden.splitlines()) if len(s) >= 25 and s not in allowed and s in prompt]
        body = []
        if c['purpose'] == 'judge':
            body = [s for s in (l.strip() for l in (row['bodies']['buggy'] + row['bodies']['fixed']).splitlines())
                    if len(s) >= 25 and s in prompt and s not in row['prompt']]
        for s in lines + body:
            own = squash(s) in seen[u]
            k = (c['purpose'], 'model_wrote_it' if own else 'NOT_FROM_MODEL', 'body' if s in body else 'hidden')
            kinds[k] += 1
            if not own and len(examples) < 10:
                examples.append((u, c['purpose'], c['round'], s))
    if u:
        seen[u] += squash(c['response'].get('message', {}).get('content', ''))
for k, v in sorted(kinds.items()):
    print(k, v)
for e in examples:
    print('EXAMPLE', e)
