"""C2 step 3 (docs/C2_PLAN.md): what happened later to the expected values that merged agent pull requests changed.

Runs in .venv-c2 (standard library and pandas). Uses the GitHub REST API through the user's logged-in `gh` CLI,
read only, instead of clones (the 122 repositories hold about 38 GB). For each merged EXPECTED_CHANGED pair of
step 1 (runs/c2/pairs.jsonl):
- the commits on the default branch that touch the test file after the merge (`commits?path=&since=`, up to
  300, oldest first), with their patch for that file (`commits/<sha>`), following renames;
- RESTORED: a later commit removes the agent's line and adds the original line back (the old expected value);
- CHANGED_AGAIN: a later commit removes the agent's line without restoring the old one (first such commit);
- at the head of the default branch: whether the agent's line is still in the file (SURVIVES) or the file is
  gone (FILE_GONE).
Lines are compared after parsing (ast.dump), so formatting and quote style do not matter; lines that do not
parse are compared with whitespace collapsed. API answers are cached in .scratch/c2_gh, so the script resumes;
it waits when fewer than 50 requests are left in the hour. Progress in runs/c2/step3_progress.json.
Writes runs/c2/step3.jsonl and review/out/c2_step3.md.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_step3.py
"""
import ast
import hashlib
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'runs' / 'c2'
CACHE = ROOT / '.scratch' / 'c2_gh'
MAX_COMMITS = 300


def norm(line):
    s = line.strip()
    try:
        return ast.dump(ast.parse(s))
    except SyntaxError:
        return re.sub(r'\s+', ' ', s)


def gh(path):
    """GET a GitHub API path through gh, cached; returns parsed JSON, or {'_error': status} on failure."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.sha1(path.encode('utf-8')).hexdigest() + '.json')
    if f.exists():
        return json.loads(f.read_text(encoding='utf-8'))
    wait_for_quota()
    for attempt in range(4):
        r = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', path], capture_output=True,
                           text=True, encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL)
        if r.returncode == 0:
            data = json.loads(r.stdout) if r.stdout.strip() else None
            break
        err = r.stderr.strip()
        if 'HTTP 404' in err or 'HTTP 409' in err or 'HTTP 422' in err or 'HTTP 451' in err:
            data = {'_error': err[:200]}
            break
        time.sleep(30 * (attempt + 1))
    else:
        raise RuntimeError(f'gh api {path} failed: {err[:300]}')
    f.write_text(json.dumps(data), encoding='utf-8')
    return data


_quota = {'checked': 0.0}


def wait_for_quota():
    if time.time() - _quota['checked'] < 60:
        return
    _quota['checked'] = time.time()
    r = subprocess.run(['gh', 'api', 'rate_limit', '--jq', '.resources.core'], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    core = json.loads(r.stdout)
    if core['remaining'] < 50:
        pause = max(0, core['reset'] - time.time()) + 30
        print(f'API quota low ({core["remaining"]} left); waiting {pause / 60:.0f} minutes', flush=True)
        time.sleep(pause)


def later_commits(repo, path, since):
    shas = []
    for page in range(1, MAX_COMMITS // 100 + 1):
        data = gh(f'repos/{repo}/commits?path={quote(path)}&since={since}&per_page=100&page={page}')
        if not isinstance(data, list):
            break
        shas += [(c['sha'], c['commit']['committer']['date'], c['commit']['message'].split('\n')[0]) for c in data]
        if len(data) < 100:
            break
    return list(reversed(shas))


def file_patch(repo, sha, path):
    data = gh(f'repos/{repo}/commits/{sha}')
    for f in (data or {}).get('files', []) if isinstance(data, dict) else []:
        if f.get('filename') == path or f.get('previous_filename') == path:
            return f
    return None


def head_lines(repo, path):
    data = gh(f'repos/{repo}/contents/{quote(path)}')
    if not isinstance(data, dict) or '_error' in data or data.get('encoding') != 'base64':
        return None
    import base64
    return {norm(x) for x in base64.b64decode(data['content']).decode('utf-8', 'replace').splitlines() if x.strip()}


def main():
    pairs = [json.loads(line) for line in open(OUT / 'pairs.jsonl', encoding='utf-8')]
    todo = [p for p in pairs if p['mode'] == 'EXPECTED_CHANGED' and p['merged']]
    merged_at = pd.read_parquet(ROOT / 'data' / 'c2' / 'pull_request.parquet', columns=['id', 'merged_at']).set_index('id').merged_at
    by_file = defaultdict(list)
    for p in todo:
        by_file[(p['repo'], p['file'], p['pr_id'])].append(p)
    results = []
    for n, ((repo, path, pr_id), ps) in enumerate(sorted(by_file.items()), 1):
        since = pd.Timestamp(merged_at[pr_id]).tz_convert('UTC').strftime('%Y-%m-%dT%H:%M:%SZ')
        state = {id(p): {'fate': None, 'sha': None, 'date': None, 'message': None} for p in ps}
        current = path
        for sha, date, msg in later_commits(repo, path, since):
            f = file_patch(repo, sha, current) or file_patch(repo, sha, path)
            if not f:
                continue
            if f.get('status') == 'renamed':
                current = f['filename']
            patch = f.get('patch') or ''
            minus = {norm(x[1:]) for x in patch.splitlines() if x.startswith('-') and not x.startswith('---')}
            plus = {norm(x[1:]) for x in patch.splitlines() if x.startswith('+') and not x.startswith('+++')}
            for p in ps:
                st = state[id(p)]
                if st['fate'] == 'RESTORED':
                    continue
                new, old = norm(p['added']), norm(p['removed'])
                if new in plus and old in minus:
                    continue  # the pull request's own change (merge commit or a re-applied copy)
                if new in minus and old in plus:
                    st.update(fate='RESTORED', sha=sha, date=date, message=msg)
                elif new in minus and st['fate'] is None:
                    st.update(fate='CHANGED_AGAIN', sha=sha, date=date, message=msg)
        head = head_lines(repo, current)
        for p in ps:
            st = state[id(p)]
            results.append({**{k: p[k] for k in ('pr_id', 'repo', 'number', 'agent', 'file', 'removed', 'added', 'url')},
                            'merged_at': since, 'fate': st['fate'] or 'UNTOUCHED', 'fate_sha': st['sha'],
                            'fate_date': st['date'], 'fate_message': st['message'],
                            'at_head': 'FILE_GONE' if head is None else ('SURVIVES' if norm(p['added']) in head else 'GONE'),
                            'old_at_head': None if head is None else norm(p['removed']) in head})
        (OUT / 'step3_progress.json').write_text(json.dumps({'done': n, 'total': len(by_file),
                                                             'updated': datetime.now(timezone.utc).isoformat()}), encoding='utf-8')
        print(f'{n}/{len(by_file)} {repo} {path}: ' + ', '.join(f"{k} {v}" for k, v in Counter(r['fate'] for r in results[-len(ps):]).items()), flush=True)
    with open(OUT / 'step3.jsonl', 'w', encoding='utf-8') as fh:
        for r in results:
            fh.write(json.dumps(r) + '\n')
    df = pd.DataFrame(results)
    lines = ['# C2 step 3: later history of the expected values changed by merged agent pull requests', '',
             'Computed by `analysis/c2_step3.py` through the GitHub API. RESTORED: a later commit on the default branch put',
             "the original line back in place of the agent's line. CHANGED_AGAIN: a later commit replaced the agent's line",
             'with something else. Counts of changed asserts; pull requests in brackets.', '',
             '| Agent | Changed asserts (PRs) | Restored | Changed again | Untouched | Agent line at head | Old line at head |',
             '|---|---|---|---|---|---|---|']
    for agent in list(df.agent.value_counts().index) + ['all']:
        s = df if agent == 'all' else df[df.agent == agent]
        cell = lambda m: f"{int(m.sum())} ({s[m].pr_id.nunique()})"
        lines.append(f"| {agent} | {len(s)} ({s.pr_id.nunique()}) | {cell(s.fate == 'RESTORED')} | {cell(s.fate == 'CHANGED_AGAIN')} | "
                     f"{cell(s.fate == 'UNTOUCHED')} | {cell(s.at_head == 'SURVIVES')} | {cell(s.old_at_head == True)} |")
    (ROOT / 'review' / 'out' / 'c2_step3.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
