"""C2 step 4: the labelling sheet for the second rater (docs/C2_PLAN.md).

Draws 100 of the 347 agent pull requests that change tests and code and change an expected value (step 1),
stratified by agent (Codex 34, Copilot 29, Devin 14, Claude Code 12, Cursor 7, Jules 4; fixed seed; v2 after
merge commits were excluded on 17 October), and writes
review/c2_labels/c2_cases.csv (UTF-8 with BOM, so Excel shows it correctly) with what a rater needs: title and
start of the description, up to three changed asserts (old and new line), the start of the code change, and the
link. The two label columns are empty (WHY: I, W, E, M or U; SAYS TEST CHANGED: Y or N). Instructions: review/c2_labels/C2_LABELLING_INSTRUCTIONS.md.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_label_sheet.py
"""
import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'c2'
OUT = ROOT / 'review' / 'c2_labels'
QUOTA = {'OpenAI_Codex': 34, 'Copilot': 29, 'Devin': 14, 'Claude_Code': 12, 'Cursor': 7, 'Google_Jules': 4}
SEED = 'gbe-c2-labels-v2'


def txt(x):
    return x if isinstance(x, str) else ''


def clean(text, limit):
    text = re.sub(r'<!--.*?-->', '', txt(text), flags=re.S)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + ' [...]'


def main():
    import sys
    sys.path.insert(0, str(ROOT / 'analysis'))
    from c2_mine import MERGE, is_test
    commits = pd.read_parquet(DATA / 'pr_commits.parquet', columns=['sha', 'pr_id', 'message'])
    skip = {(r.pr_id, r.sha) for r in commits.itertuples() if MERGE.match(str(r.message))}
    prs = pd.read_csv(ROOT / 'runs' / 'c2' / 'prs.csv')
    pool = prs[prs.expected_changes > 0]
    rng = random.Random(SEED)
    chosen = []
    for agent, n in QUOTA.items():
        ids = sorted(pool[pool.agent == agent].pr_id)
        chosen += rng.sample(ids, n)
    rng.shuffle(chosen)
    pairs = defaultdict(list)
    for line in open(ROOT / 'runs' / 'c2' / 'pairs.jsonl', encoding='utf-8'):
        p = json.loads(line)
        if p['mode'] == 'EXPECTED_CHANGED' and p['pr_id'] in set(chosen):
            pairs[p['pr_id']].append(p)
    meta = pd.read_parquet(DATA / 'pull_request.parquet', columns=['id', 'title', 'body', 'html_url', 'state', 'merged_at'])
    meta = meta[meta.id.isin(chosen)].set_index('id')
    code = defaultdict(list)
    f = pq.ParquetFile(DATA / 'pr_commit_details.parquet')
    for batch in f.iter_batches(batch_size=50_000, columns=['pr_id', 'sha', 'filename', 'patch']):
        df = batch.to_pandas()
        df = df[df.pr_id.isin(chosen) & df.filename.str.endswith('.py', na=False)]
        for r in df.itertuples(index=False):
            if not is_test(r.filename) and isinstance(r.patch, str) and (r.pr_id, r.sha) not in skip:
                code[r.pr_id].append(f'--- {r.filename}\n{r.patch}')
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, pid in enumerate(chosen, 1):
        m = meta.loc[pid]
        asserts = []
        seen = set()
        for p in pairs[pid]:
            if (p['removed'], p['added']) in seen:
                continue
            seen.add((p['removed'], p['added']))
            asserts.append(f"OLD: {p['removed']}\nNEW: {p['added']}")
        n_more = len(seen) - 3
        changed = '\n\n'.join(asserts[:3]) + (f'\n\n(+{n_more} more changed asserts in this PR)' if n_more > 0 else '')
        rows.append({'case': f'C{i:03d}', 'agent': pid and pool.set_index('pr_id').at[pid, 'agent'],
                     'merged': 'yes' if pd.notna(m.merged_at) else 'no', 'link': m.html_url,
                     'title': txt(m.title), 'description_start': clean(m.body, 900),
                     'changed_asserts': changed, 'code_change_start': clean('\n'.join(code[pid]), 900) or '(code patch not in the dataset; open the link)',
                     'WHY (I / W / E / M / U)': '', 'SAYS TEST CHANGED (Y / N)': '', 'note (optional)': ''})
    with open(OUT / 'c2_cases.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (OUT / 'c2_sample.json').write_text(json.dumps({'seed': SEED, 'quota': QUOTA, 'pr_ids': [int(x) for x in chosen]}, indent=1),
                                        encoding='utf-8')
    print(f'{len(rows)} cases written to {OUT / "c2_cases.csv"}')


if __name__ == '__main__':
    main()
