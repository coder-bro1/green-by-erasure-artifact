"""C2 step 1 (docs/C2_PLAN.md): agent pull requests in Python repositories that change the expected value of an
existing test together with the code.

Runs in .venv-c2 (pandas, pyarrow). Input: the AIDev v4 tables in data/c2. A pull request counts when its
repository's main language is Python and its commits change at least one test file and one other Python file.
Commits whose message starts like a merge ("Merge branch ...", "Merge pull request ...", "Merge ... into ...") are
skipped: they carry other people's changes. A commit found in several pull requests counts only for the
earliest one. Test files: .py files named test_*.py or *_test.py, or under a tests/ or test/ folder, or conftest.py.

Expected-value change, per hunk of a test-file patch: a removed and an added line that both parse as a single
assert statement of the same kind, where one side is unchanged and the other differs:
- `assert A <op> B` with the same comparison operator: A unchanged and B changed, or B unchanged and A changed;
- `self.assertX(a, b, ...)` (assertEqual, assertAlmostEqual, assertListEqual, assertDictEqual, assertIn, ...):
  same method, one of the first two arguments unchanged, the other changed.
Pairs are matched greedily in order within a hunk. Multi-line asserts are not seen, so counts are lower bounds.
Also counted per test file: assert lines removed without a replacement (net loss of assert lines) and added
skip or xfail markers.

Outputs in runs/c2: pairs.jsonl (one record per expected-value change, with pull request, commit, file and the
two lines), prs.csv (one row per Python pull request that touches tests and code) and review/out/c2_step1.md.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_mine.py
"""
import ast
import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'c2'
OUT = ROOT / 'runs' / 'c2'
TEST_PATH = re.compile(r'(^|/)(tests?/.*\.py|test_[^/]*\.py|[^/]*_test\.py|conftest\.py)$')
MERGE = re.compile(r'^\s*Merge (branch|remote-tracking branch|pull request|.* into )', re.I)
# Authorship (19 October, after the commit-level inspection of the possible erasures): agent pull requests also
# carry upstream commits brought in by rebases ("... (#405)"), merge commits with other messages ("merge",
# "Merge remote changes ...") and human fix-ups. Only the agent's own commits count: for the agents that commit
# under a bot account, commits by that account; for Codex and Claude Code, which commit under the user's name,
# commits by the pull request's opener (or signed "Claude AI"). Upstream squash commits and messages starting
# with "merge" are dropped for every agent.
AGENT_AUTHORS = {'Copilot': {'Copilot', 'copilot-swe-agent[bot]'}, 'Devin': {'devin-ai-integration[bot]'},
                 'Cursor': {'cursoragent', 'Cursor Agent'}, 'Google_Jules': {'google-labs-jules[bot]'}}
USER_AGENTS = {'OpenAI_Codex', 'Claude_Code'}
UPSTREAM = re.compile(r'\(#\d+\)\s*$')
MERGEISH = re.compile(r'^\s*merge\b', re.I)
HUNK = re.compile(r'^@@ .*? @@', re.M)
SKIP = re.compile(r'^\+\s*@pytest\.mark\.(skip|skipif|xfail)\b|^\+\s*@unittest\.skip|^\+.*\bpytest\.(skip|xfail)\(', re.M)
UNITTEST_TWO_ARG = {'assertEqual', 'assertEquals', 'assertNotEqual', 'assertAlmostEqual', 'assertNotAlmostEqual',
                    'assertListEqual', 'assertDictEqual', 'assertTupleEqual', 'assertSetEqual', 'assertSequenceEqual',
                    'assertMultiLineEqual', 'assertCountEqual', 'assertIn', 'assertNotIn', 'assertIs', 'assertIsNot',
                    'assertGreater', 'assertGreaterEqual', 'assertLess', 'assertLessEqual', 'assertRaisesRegex'}


def is_test(path):
    return bool(TEST_PATH.search(path))


def parts(line):
    """(kind, a, b) of a one-line assert, or None. a and b are normalised source strings."""
    code = line.strip()
    if not code or code.startswith('#'):
        return None
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    if len(tree.body) != 1:
        return None
    node = tree.body[0]
    if isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare) and len(node.test.ops) == 1:
        return ('assert ' + type(node.test.ops[0]).__name__, ast.unparse(node.test.left),
                ast.unparse(node.test.comparators[0]))
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        f = node.value.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, 'id', '')
        if name in UNITTEST_TWO_ARG and len(node.value.args) >= 2:
            return name, ast.unparse(node.value.args[0]), ast.unparse(node.value.args[1])
    return None


def is_assert(line):
    s = line.strip()
    return s.startswith('assert') or s.startswith('self.assert') or '.assert' in s[:40]


def expected_changes(patch):
    """Expected-value changes in one patch, as (removed line, added line, unchanged side)."""
    found = []
    for hunk in HUNK.split(patch or '')[1:]:
        removed, added = [], []
        for line in hunk.splitlines():
            if line.startswith('-') and not line.startswith('---'):
                p = parts(line[1:])
                if p:
                    removed.append((line[1:].strip(), p))
            elif line.startswith('+') and not line.startswith('+++'):
                p = parts(line[1:])
                if p:
                    added.append((line[1:].strip(), p))
        used = set()
        for r_line, (kind, a, b) in removed:
            for j, (a_line, (kind2, a2, b2)) in enumerate(added):
                if j in used or kind != kind2 or (a, b) == (a2, b2):
                    continue
                if (a == a2) != (b == b2):
                    used.add(j)
                    same, old, new = (a, b, b2) if a == a2 else (b, a, a2)
                    found.append((r_line, a_line, same, mode(same, new)))
                    break
    return found


def has_call(src):
    try:
        return any(isinstance(n, ast.Call) for n in ast.walk(ast.parse(src, mode='eval')))
    except SyntaxError:
        return False


def is_literal(src):
    try:
        ast.literal_eval(src)
        return True
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        return False


def mode(unchanged, changed):
    """EXPECTED_CHANGED when the side that computes (a call, or a name compared with a literal) stayed and the
    expected side changed; INPUT_CHANGED when the computing side changed; AMBIGUOUS otherwise."""
    if has_call(unchanged) and not has_call(changed):
        return 'EXPECTED_CHANGED'
    if has_call(changed) and not has_call(unchanged):
        return 'INPUT_CHANGED'
    if not has_call(unchanged) and not has_call(changed):
        if is_literal(changed) and not is_literal(unchanged):
            return 'EXPECTED_CHANGED'
        if is_literal(unchanged) and not is_literal(changed):
            return 'INPUT_CHANGED'
    return 'AMBIGUOUS'


def assert_balance(patch):
    lines = (patch or '').splitlines()
    removed = sum(1 for x in lines if x.startswith('-') and not x.startswith('---') and is_assert(x[1:]))
    added = sum(1 for x in lines if x.startswith('+') and not x.startswith('+++') and is_assert(x[1:]))
    return removed, added


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    repo = pd.read_parquet(DATA / 'repository.parquet', columns=['id', 'full_name', 'language', 'stars'])
    pr = pd.read_parquet(DATA / 'pull_request.parquet',
                         columns=['id', 'number', 'title', 'agent', 'state', 'created_at', 'merged_at', 'repo_id', 'html_url',
                                  'user'])
    pr = pr.merge(repo.rename(columns={'id': 'repo_id'}), on='repo_id', how='left')
    py = pr[pr.language == 'Python'].set_index('id')
    ids = set(py.index)
    commits = pd.read_parquet(DATA / 'pr_commits.parquet', columns=['sha', 'pr_id', 'message', 'author'])
    # Merge commits (for example "Merge branch 'main' into feature") bring other people's changes into the pull
    # request's commit list; their diffs are not the agent's edits and are skipped (found on 17 October, when
    # 636 of 2,052 expected-value changes turned out to come from such commits).
    merge = {(r.pr_id, r.sha) for r in commits[commits.pr_id.isin(ids)].itertuples() if MERGE.match(str(r.message))}
    commits = commits[[(p, s) not in merge for p, s in zip(commits.pr_id, commits.sha)]]
    agent_of = py.agent.to_dict()
    opener = py.user.to_dict()

    def foreign_commit(pr_id, author, message):
        first_line = str(message).split('\n', 1)[0]
        if UPSTREAM.search(first_line) or MERGEISH.match(first_line):
            return True
        agent = agent_of.get(pr_id)
        if agent in AGENT_AUTHORS:
            return author not in AGENT_AUTHORS[agent]
        if agent in USER_AGENTS:
            return author not in {opener.get(pr_id), 'Claude AI', 'Claude'}
        return False
    foreign = {(r.pr_id, r.sha) for r in commits[commits.pr_id.isin(ids)].itertuples()
               if foreign_commit(r.pr_id, r.author, r.message)}
    commits = commits[[(p, s) not in foreign for p, s in zip(commits.pr_id, commits.sha)]]
    # A commit that sits in several pull requests (a branch built on another branch) counts once, for the
    # earliest of those pull requests.
    created = pr.set_index('id').created_at if 'created_at' in pr else None
    first = {}
    for p_, s_ in zip(commits.pr_id, commits.sha):
        if s_ not in first or created[p_] < created[first[s_]]:
            first[s_] = p_
    inherited = {(p_, s_) for p_, s_ in zip(commits.pr_id, commits.sha) if first[s_] != p_}
    commits = commits[[(p_, s_) not in inherited for p_, s_ in zip(commits.pr_id, commits.sha)]]
    order = {(p, s): i for p, grp in commits[commits.pr_id.isin(ids)].groupby('pr_id', sort=False)
             for i, s in enumerate(grp.sha)}
    n_commits = commits[commits.pr_id.isin(ids)].groupby('pr_id').size().to_dict()
    per_pr = defaultdict(lambda: {'test_files': set(), 'src_files': set(), 'src_commits': set(), 'pairs': 0,
                                  'pair_commits': set(), 'asserts_removed': 0, 'asserts_added': 0, 'skips_added': 0,
                                  'patch_missing': 0, 'EXPECTED_CHANGED': 0, 'INPUT_CHANGED': 0, 'AMBIGUOUS': 0})
    pairs_out = open(OUT / 'pairs.jsonl', 'w', encoding='utf-8')
    f = pq.ParquetFile(DATA / 'pr_commit_details.parquet')
    n_rows = n_merge_rows = 0
    for batch in f.iter_batches(batch_size=50_000, columns=['pr_id', 'sha', 'filename', 'status', 'patch']):
        df = batch.to_pandas()
        n_rows += len(df)
        df = df[df.pr_id.isin(ids) & df.filename.str.endswith('.py', na=False)]
        for row in df.itertuples(index=False):
            if (row.pr_id, row.sha) in merge or (row.pr_id, row.sha) in inherited or (row.pr_id, row.sha) in foreign:
                n_merge_rows += 1
                continue
            rec = per_pr[row.pr_id]
            if not is_test(row.filename):
                rec['src_files'].add(row.filename)
                rec['src_commits'].add(row.sha)
                continue
            rec['test_files'].add(row.filename)
            if not isinstance(row.patch, str):
                rec['patch_missing'] += 1
                continue
            r, a = assert_balance(row.patch)
            rec['asserts_removed'] += r
            rec['asserts_added'] += a
            rec['skips_added'] += len(SKIP.findall(row.patch))
            for removed, added, same, kind in expected_changes(row.patch):
                rec[kind] += 1
                if kind == 'EXPECTED_CHANGED':
                    rec['pairs'] += 1
                    rec['pair_commits'].add(row.sha)
                meta = py.loc[row.pr_id]
                pairs_out.write(json.dumps({'pr_id': int(row.pr_id), 'repo': meta.full_name, 'number': int(meta.number),
                                            'agent': meta.agent, 'merged': bool(pd.notna(meta.merged_at)),
                                            'sha': row.sha, 'commit_index': order.get((row.pr_id, row.sha)),
                                            'file': row.filename, 'removed': removed, 'added': added,
                                            'unchanged_side': same, 'mode': kind, 'url': meta.html_url}) + '\n')
        print(f'{n_rows:,} rows read, {len(per_pr):,} Python pull requests seen', flush=True)
    pairs_out.close()
    rows = []
    for pid, rec in per_pr.items():
        if not rec['test_files'] or not rec['src_files']:
            continue
        meta = py.loc[pid]
        idx_src = [order.get((pid, s)) for s in rec['src_commits']]
        idx_pair = [order.get((pid, s)) for s in rec['pair_commits']]
        later = bool(idx_pair) and None not in idx_src + idx_pair and min(idx_pair) > min(idx_src) \
            and not (rec['pair_commits'] & rec['src_commits'])
        rows.append({'pr_id': pid, 'repo': meta.full_name, 'number': meta.number, 'agent': meta.agent, 'state': meta.state,
                     'merged': bool(pd.notna(meta.merged_at)), 'stars': meta.stars, 'test_files': len(rec['test_files']),
                     'src_files': len(rec['src_files']), 'commits': n_commits.get(pid, 0),
                     'expected_changes': rec['pairs'], 'input_changes': rec['INPUT_CHANGED'],
                     'ambiguous_changes': rec['AMBIGUOUS'], 'test_edit_after_code_commit': later,
                     'asserts_removed': rec['asserts_removed'], 'asserts_added': rec['asserts_added'],
                     'net_asserts_lost': max(0, rec['asserts_removed'] - rec['asserts_added']),
                     'skips_added': rec['skips_added'], 'test_patches_missing': rec['patch_missing'],
                     'title': meta.title, 'url': meta.html_url})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / 'prs.csv', index=False)
    lines = ['# C2 step 1: expected-value changes in agent pull requests (AIDev-pop, Python)', '',
             'Computed by `analysis/c2_mine.py`. A pull request counts when it changes a test file and another Python',
             'file. Expected-value change: a one-line assert whose checked side is unchanged and whose other side changed.', '',
             f'Python pull requests in AIDev-pop: {len(py):,} (merged {py.merged_at.notna().sum():,}); diff rows read: {n_rows:,}; '
             f'Python file diffs skipped: {n_merge_rows:,} (from {len(merge):,} merge commits, {len(foreign):,} commits not by the agent '
             f'and {len(inherited):,} commits that belong to an earlier pull request).', '',
             '| Agent | Python PRs | Touch tests and code | With an expected-value change | Merged, of those | Test edit in a later commit than the code | Expected-value changes | PRs adding skip or xfail |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for agent in list(py.agent.value_counts().index) + ['all']:
        allp = py if agent == 'all' else py[py.agent == agent]
        sub = out if agent == 'all' else out[out.agent == agent]
        ch = sub[sub.expected_changes > 0]
        lines.append(f'| {agent} | {len(allp):,} | {len(sub):,} | {len(ch):,} ({100 * len(ch) / max(1, len(sub)):.0f}%) | '
                     f'{int(ch.merged.sum()):,} | {int(ch.test_edit_after_code_commit.sum()):,} | {int(ch.expected_changes.sum()):,} | '
                     f'{int((sub.skips_added > 0).sum()):,} |')
    lines += ['', f"Test-file patches missing from AIDev (too large for the GitHub API): {int(out.test_patches_missing.sum()):,}."]
    (ROOT / 'review' / 'out' / 'c2_step1.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
