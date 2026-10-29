"""C2 step 2 (docs/C2_PLAN.md): do agent pull requests that change an expected value say so, and did a human
reviewer look at the change?

Runs in .venv-c2. Inputs: runs/c2/prs.csv and runs/c2/pairs.jsonl (step 1) and the AIDev tables pull_request,
pr_reviews, pr_review_comments and pr_comments. Groups: pull requests that touch tests and code and change an
expected value (EXPECTED_CHANGED, step 1), against those that touch tests and code without one.

Per pull request:
- mentions_tests: the title or body uses the word test(s) or assert;
- explains_test_change: the title or body says that tests or expectations were changed (a change verb within
  40 characters of test, assert or expect, in either order, or "to match/reflect the new/actual ..."). Checked
  by hand on a sample (review/out/c2_step2_sample.md);
- human_comment: any comment or review body by a user of type User;
- human_review_on_test_file: an inline review comment by a User on a test file whose expected value changed;
- human_review_on_line: such a comment anchored on one of the changed assert lines (GitHub ends a review
  comment's diff hunk at the line it is attached to, so the hunk's last line is compared; corrected on 18 October,
  review item R5);
- human_review_in_context: such a comment whose diff hunk shows one of the changed assert lines anywhere (the
  measure first reported as "on the changed line");
- changes_requested: a review by a User in state CHANGES_REQUESTED.
Writes runs/c2/step2.csv and review/out/c2_step2.md. Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_step2.py
"""
import json
import random
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'c2'
OUT = ROOT / 'runs' / 'c2'
VERB = r'(updat|adjust|chang|modif|fix|correct|align|rewr|revis|tweak|amend)\w*'
NOUN = r'(tests?|assert\w*|expect\w*)'
EXPLAINS = re.compile(rf'\b{VERB}\b[^.\n]{{0,40}}\b{NOUN}\b|\b{NOUN}\b[^.\n]{{0,40}}\b{VERB}\b|'
                      r'\bto (match|reflect)\b[^.\n]{0,30}\b(new|updated|current|actual|changed)\b', re.I)
MENTIONS = re.compile(r'\btests?\b|\bassert', re.I)
URL = re.compile(r'repos/([^/]+/[^/]+)/pulls/(\d+)$')


def txt(x):
    """Missing text comes from Parquet as None or NaN."""
    return x if isinstance(x, str) else ''


def norm(line):
    return re.sub(r'\s+', ' ', line.strip())


def main():
    prs = pd.read_csv(OUT / 'prs.csv')
    pairs = [json.loads(line) for line in open(OUT / 'pairs.jsonl', encoding='utf-8')]
    exp = [p for p in pairs if p['mode'] == 'EXPECTED_CHANGED']
    files = defaultdict(set)
    lines = defaultdict(set)
    for p in exp:
        files[p['pr_id']].add(p['file'])
        lines[p['pr_id']].add(norm(p['added']))
    meta = pd.read_parquet(DATA / 'pull_request.parquet', columns=['id', 'title', 'body', 'number', 'repo_url'])
    meta = meta[meta.id.isin(set(prs.pr_id))].set_index('id')
    key = {(r.repo, int(r.number)): r.pr_id for r in prs.itertuples()}
    reviews = pd.read_parquet(DATA / 'pr_reviews.parquet', columns=['pr_id', 'user_type', 'state', 'body'])
    reviews = reviews[reviews.pr_id.isin(set(prs.pr_id))]
    comments = pd.read_parquet(DATA / 'pr_comments.parquet', columns=['pr_id', 'user_type', 'body'])
    comments = comments[comments.pr_id.isin(set(prs.pr_id))]
    inline = pd.read_parquet(DATA / 'pr_review_comments.parquet', columns=['user_type', 'path', 'diff_hunk', 'pull_request_url', 'body'])
    inline['pr_id'] = [key.get((m.group(1), int(m.group(2)))) if (m := URL.search(txt(u))) else None for u in inline.pull_request_url]
    inline = inline[inline.pr_id.notna()]
    human_reviews = reviews[reviews.user_type == 'User']
    human_any = set(human_reviews.pr_id) | set(comments[comments.user_type == 'User'].pr_id) | set(inline[inline.user_type == 'User'].pr_id)
    changes_req = set(human_reviews[human_reviews.state == 'CHANGES_REQUESTED'].pr_id)
    on_file, on_line, in_context = set(), set(), set()
    for r in inline[inline.user_type == 'User'].itertuples():
        pid = int(r.pr_id)
        if r.path in files.get(pid, ()):
            on_file.add(pid)
            hunk_lines = txt(r.diff_hunk).splitlines()
            hunk = {norm(x[1:]) for x in hunk_lines if x.startswith('+')}
            if hunk & lines[pid]:
                in_context.add(pid)
            if hunk_lines and hunk_lines[-1].startswith('+') and norm(hunk_lines[-1][1:]) in lines[pid]:
                on_line.add(pid)
    rows = []
    for r in prs.itertuples():
        text = txt(meta.at[r.pr_id, 'title']) + '\n' + txt(meta.at[r.pr_id, 'body']) if r.pr_id in meta.index else ''
        rows.append({'pr_id': r.pr_id, 'agent': r.agent, 'merged': r.merged, 'expected_change': r.expected_changes > 0,
                     'mentions_tests': bool(MENTIONS.search(text)), 'explains_test_change': bool(EXPLAINS.search(text)),
                     'human_comment': r.pr_id in human_any, 'human_review_on_test_file': r.pr_id in on_file,
                     'human_review_on_line': r.pr_id in on_line, 'human_review_in_context': r.pr_id in in_context,
                     'changes_requested': r.pr_id in changes_req,
                     'url': r.url})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / 'step2.csv', index=False)
    pct = lambda s: f'{int(s.sum()):,} ({100 * s.mean():.0f}%)' if len(s) else '-'
    out = ['# C2 step 2: disclosure and review of expected-value changes', '',
           'Computed by `analysis/c2_step2.py`. Pull requests by agents in Python repositories of AIDev-pop that change',
           'a test file and other code; "with" = at least one expected-value change in an existing assert (step 1).', '',
           '| Agent | Group | PRs | Mentions tests | Explains a test change | Any human comment | Human review comment on the changed test file | Its diff context shows the changed assert | Anchored on the changed assert | Changes requested | Merged |',
           '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for agent in list(df.agent.value_counts().index) + ['all']:
        for grp, label in ((True, 'with'), (False, 'without')):
            s = df[(df.expected_change == grp) & ((df.agent == agent) if agent != 'all' else True)]
            if not len(s):
                continue
            out.append(f"| {agent} | {label} | {len(s):,} | {pct(s.mentions_tests)} | {pct(s.explains_test_change)} | "
                       f"{pct(s.human_comment)} | {pct(s.human_review_on_test_file) if grp else '-'} | "
                       f"{pct(s.human_review_in_context) if grp else '-'} | {pct(s.human_review_on_line) if grp else '-'} | "
                       f"{pct(s.changes_requested)} | {pct(s.merged)} |")
    (ROOT / 'review' / 'out' / 'c2_step2.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('\n'.join(out))
    # Sample for a hand check of the disclosure flag: 15 flagged and 15 not flagged, with the matched text.
    random.seed(20261016)
    w = df[df.expected_change]
    sample = random.sample(list(w[w.explains_test_change].pr_id), 15) + random.sample(list(w[~w.explains_test_change].pr_id), 15)
    s_lines = ['# C2 step 2: hand check of the disclosure flag', '']
    for pid in sample:
        text = txt(meta.at[pid, 'title']) + '\n' + txt(meta.at[pid, 'body'])
        m = EXPLAINS.search(text)
        s_lines += [f"## {pid} flag={bool(m)} match={m.group(0)!r}" if m else f'## {pid} flag=False',
                    '', '```', text[:1500], '```', '', 'Changed asserts:', '']
        s_lines += [f"- `{p['removed'][:120]}` -> `{p['added'][:120]}`" for p in exp if p['pr_id'] == pid][:4] + ['']
    (ROOT / 'review' / 'out' / 'c2_step2_sample.md').write_text('\n'.join(s_lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
