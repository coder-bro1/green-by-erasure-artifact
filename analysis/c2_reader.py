"""C2 step 4: a readable HTML view of the 100 labelling cases (review/c2_labels/C2_CASES_READER.html).

Read-only companion to review/c2_labels/c2_cases.csv; labels still go into the CSV. Per case: title and full
description, every changed assert with the changed part marked, the code change of the pull request (non-test
Python files, merge commits left out, each file cut after 120 lines), the link, and a fixed checklist. Neutral
aids only: names from the changed asserts are highlighted where they occur in the title or description, and a
pair of asserts that trade places is pointed out as a fact. Nothing in the page comes from either rater's labels.
Runs in .venv-c2. Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_reader.py
"""
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from c2_mine import MERGE, is_test  # noqa: E402

DATA = ROOT / 'data' / 'c2'
OUT = ROOT / 'review' / 'c2_labels' / 'C2_CASES_READER.html'
DEFAULT_INTRO = ('The same 100 cases as <code>c2_cases.csv</code>, easier to read. Labels still go into the CSV. '
                 'Yellow marks the part of an assert that changed; highlighted names in the description are names that '
                 'also occur in the changed asserts. The rules are in <code>C2_LABEL_GUIDE.html</code>.')
COMMON = {'assert', 'self', 'result', 'results', 'assertequal', 'assertin', 'true', 'false', 'none', 'response',
          'data', 'value', 'values', 'len', 'str', 'lower', 'json', 'text', 'output', 'expected', 'call_count'}


def esc(s):
    return html.escape(s if isinstance(s, str) else '')


def marked(old, new):
    """Both lines with the differing middle part wrapped in <mark>."""
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]:
        i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
        j += 1
    def wrap(s):
        end = len(s) - j
        return esc(s[:i]) + '<mark>' + esc(s[i:end]) + '</mark>' + esc(s[end:])
    return wrap(old), wrap(new)


def names(lines):
    found = set()
    for line in lines:
        for w in re.findall(r'[A-Za-z_][A-Za-z0-9_]{3,}', line):
            if w.lower() not in COMMON:
                found.add(w)
    return found


def highlight(text, words):
    out = esc(text)
    for w in sorted(words, key=len, reverse=True):
        out = re.sub(rf'(?<![A-Za-z0-9_]){re.escape(esc(w))}(?![A-Za-z0-9_])', f'<span class="hl">{esc(w)}</span>', out)
    return out


def diff_html(patch, limit=120):
    lines = patch.splitlines()
    shown = lines[:limit]
    rows = []
    for line in shown:
        cls = 'add' if line.startswith('+') else 'del' if line.startswith('-') else 'hunk' if line.startswith('@@') else 'file' if line.startswith('--- ') else ''
        rows.append(f'<span class="{cls}">{esc(line)}</span>')
    if len(lines) > limit:
        rows.append(f'<span class="hunk">... {len(lines) - limit} more lines; open the link for the full change</span>')
    return '\n'.join(rows)


def main(out=OUT, only=None, labels=None, heading='C2 cases reader', intro=None):
    """Write the reader; `only` limits it to some cases, `labels` maps a case to an HTML block shown under its title."""
    cases = pd.read_csv(ROOT / 'review' / 'c2_labels' / 'c2_cases.csv', encoding='utf-8-sig', usecols=['case', 'link'])
    sample = json.loads((ROOT / 'review' / 'c2_labels' / 'c2_sample.json').read_text(encoding='utf-8'))['pr_ids']
    meta = pd.read_parquet(DATA / 'pull_request.parquet', columns=['id', 'title', 'body', 'html_url', 'agent', 'merged_at'])
    meta = meta[meta.id.isin(sample)].set_index('id')
    assert [meta.at[p, 'html_url'] for p in sample] == list(cases.link), 'sheet and sample out of order'
    pairs = defaultdict(list)
    for line in open(ROOT / 'runs' / 'c2' / 'pairs.jsonl', encoding='utf-8'):
        p = json.loads(line)
        if p['mode'] == 'EXPECTED_CHANGED' and p['pr_id'] in set(sample):
            pairs[p['pr_id']].append(p)
    commits = pd.read_parquet(DATA / 'pr_commits.parquet', columns=['sha', 'pr_id', 'message'])
    skip = {(r.pr_id, r.sha) for r in commits.itertuples() if MERGE.match(str(r.message))}
    code = defaultdict(list)
    f = pq.ParquetFile(DATA / 'pr_commit_details.parquet')
    for batch in f.iter_batches(batch_size=50_000, columns=['pr_id', 'sha', 'filename', 'patch']):
        df = batch.to_pandas()
        df = df[df.pr_id.isin(sample) & df.filename.str.endswith('.py', na=False)]
        for r in df.itertuples(index=False):
            if not is_test(r.filename) and isinstance(r.patch, str) and (r.pr_id, r.sha) not in skip:
                code[r.pr_id].append(f'--- {r.filename}\n{r.patch}')
    cards, nav = [], []
    for case, pid in zip(cases.case, sample):
        if only is not None and case not in only:
            continue
        m = meta.loc[pid]
        seen, rows = set(), []
        lines_all = []
        for p in pairs[pid]:
            key = (p['removed'], p['added'])
            if key in seen:
                continue
            seen.add(key)
            lines_all += [p['removed'], p['added']]
            o, n = marked(p['removed'], p['added'])
            rows.append(f'<div class="pair"><div class="file">{esc(p["file"])}</div>'
                        f'<div class="old"><b>OLD</b> {o}</div><div class="new"><b>NEW</b> {n}</div></div>')
        swaps = sum(1 for a, b in seen if (b, a) in seen) // 2
        swap_note = (f'<p class="fact">Fact: {swaps} pair{"s" if swaps > 1 else ""} of these lines trade places '
                     '(one line becomes the other and back).</p>') if swaps else ''
        words = names(lines_all)
        body_hl = highlight(m.body, words) if isinstance(m.body, str) else '<i>(no description)</i>'
        title_hl = highlight(m.title, words)
        in_text = sorted(w for w in words if re.search(rf'(?<![A-Za-z0-9_]){re.escape(w)}(?![A-Za-z0-9_])',
                                                       f"{m.title}\n{m.body if isinstance(m.body, str) else ''}"))
        found_note = (f'<p class="fact">Names from the changed asserts that appear in the title or description: '
                      f'{", ".join(f"<code>{esc(w)}</code>" for w in in_text)} (highlighted below).</p>'
                      if in_text else '<p class="fact">None of the names in the changed asserts appears in the title or description.</p>')
        patch = '\n'.join(code[pid])
        code_html = diff_html(patch) if patch else '<span class="hunk">(no code patch in the dataset; open the link)</span>'
        merged = 'merged' if pd.notna(m.merged_at) else 'not merged'
        nav.append(f'<a href="#{case}">{case}</a>')
        cards.append(f'''
<section class="case" id="{case}">
  <header><span class="id">{case}</span><span class="meta">{esc(m.agent)} · {merged}</span>
  <a class="link" href="{esc(m.html_url)}" target="_blank" rel="noopener">open on GitHub ↗</a></header>
  <h2>{title_hl}</h2>
  {(labels or {}).get(case, '')}
  <div class="check"><b>Check in order:</b> 1 same expectation written differently? (M) · 2 does the PR announce
  this behaviour? (I) · 3 old value wrong for a reason outside the code: fixture, mock, test data, library, the
  agent's own new test? (W) · 4 test now agrees with new code with no reason, against stated intent, or loosened? (E) · else U.
  Then: does the text say existing expectations changed? (Y/N)</div>
  <h3>Changed asserts ({len(seen)})</h3>
  {swap_note}{''.join(rows)}
  <h3>Title and description</h3>
  {found_note}
  <div class="desc">{body_hl}</div>
  <details><summary>Code change of the pull request (test files left out)</summary><pre class="diff">{code_html}</pre></details>
</section>''')
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(heading).title()}</title>
<style>
:root {{ --bg:#fbfaf7; --panel:#fff; --text:#1d1d1b; --muted:#5c5a55; --line:#e4e1d9; --code:#f4f2ed;
  --add:#e3f4e8; --addt:#1f6b3a; --del:#fbe6e4; --delt:#9b2c24; --hl:#fff1b8; --mark:#ffd27a; --accent:#2f5d8a; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#171716; --panel:#201f1d; --text:#ecebe6;
  --muted:#a8a59d; --line:#34322e; --code:#26251f; --add:#1d3326; --addt:#8fd3a8; --del:#3a2220; --delt:#f2a49c;
  --hl:#4a4020; --mark:#7a5a12; --accent:#8db4dc; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:15.5px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
nav {{ position:sticky; top:0; z-index:2; background:var(--panel); border-bottom:1px solid var(--line); padding:8px 16px;
  display:flex; flex-wrap:wrap; gap:4px 8px; font-size:.85rem; max-height:96px; overflow:auto; }}
nav a {{ color:var(--accent); text-decoration:none; }}
main {{ max-width:960px; margin:0 auto; padding:16px 16px 80px; }}
.case {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:16px 18px; margin:20px 0; scroll-margin-top:110px; }}
.case header {{ display:flex; flex-wrap:wrap; gap:10px; align-items:baseline; }}
.id {{ font-weight:800; font-size:1.1rem; }} .meta {{ color:var(--muted); }}
.link {{ margin-left:auto; color:var(--accent); }}
h2 {{ font-size:1.15rem; margin:8px 0 10px; }} h3 {{ font-size:.95rem; margin:16px 0 6px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
.check {{ background:var(--code); border-radius:8px; padding:8px 10px; font-size:.88rem; color:var(--muted); }}
.pair {{ border:1px solid var(--line); border-radius:8px; margin:8px 0; overflow:hidden; font:13.5px/1.45 ui-monospace,Consolas,monospace; }}
.pair .file {{ padding:4px 10px; color:var(--muted); font-size:12px; border-bottom:1px solid var(--line); word-break:break-all; }}
.old, .new {{ padding:5px 10px; white-space:pre-wrap; word-break:break-word; }}
.old {{ background:var(--del); color:var(--delt); }} .new {{ background:var(--add); color:var(--addt); }}
.old b, .new b {{ font-weight:700; margin-right:6px; }}
mark {{ background:var(--mark); color:inherit; border-radius:3px; padding:0 1px; }}
.fact {{ font-size:.9rem; color:var(--muted); margin:6px 0; }}
.desc {{ white-space:pre-wrap; word-break:break-word; background:var(--code); border-radius:8px; padding:10px 12px; max-height:420px; overflow:auto; font-size:.92rem; }}
.hl {{ background:var(--hl); border-radius:3px; }}
details {{ margin-top:12px; }} summary {{ cursor:pointer; color:var(--accent); }}
pre.diff {{ background:var(--code); border-radius:8px; padding:10px 12px; overflow:auto; max-height:520px; font:12.5px/1.45 ui-monospace,Consolas,monospace; }}
pre.diff span {{ display:block; white-space:pre-wrap; word-break:break-word; }}
.add {{ background:var(--add); color:var(--addt); }} .del {{ background:var(--del); color:var(--delt); }}
.hunk {{ color:var(--muted); }} .file {{ font-weight:700; }}
.intro {{ color:var(--muted); }}
.labels {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:6px 0 12px; }}
.labels div {{ border:1px solid var(--line); border-radius:8px; padding:8px 10px; font-size:.92rem; }}
.labels b.l {{ font-size:1.05rem; }}
@media (max-width:640px) {{ .labels {{ grid-template-columns:1fr; }} }}
</style></head><body>
<nav>{" ".join(nav)}</nav>
<main>
<h1>{esc(heading)}</h1>
<p class="intro">{intro or DEFAULT_INTRO}</p>
{"".join(cards)}
</main></body></html>'''
    out.write_text(page, encoding='utf-8')
    print(f'{len(cards)} cases written to {out} ({out.stat().st_size / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
