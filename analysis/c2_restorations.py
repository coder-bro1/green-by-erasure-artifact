"""C2: material for reading the restoration cases of step 3 by hand.

For every merged pull request with a RESTORED expected value (runs/c2/step3.jsonl) this collects, through the
cached GitHub API helper of c2_step3.py: the pull request's title, body and changed files; the restoring commit's
message, author and changed files (test or other); whether that commit also changes the non-test files the pull
request changed; and the restored lines. Writes review/out/c2_restorations.md for reading.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_restorations.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from c2_mine import is_test  # noqa: E402
from c2_step3 import gh  # noqa: E402


def main():
    rows = [json.loads(line) for line in open(ROOT / 'runs' / 'c2' / 'step3.jsonl', encoding='utf-8')]
    cases = defaultdict(list)
    for r in rows:
        if r['fate'] == 'RESTORED':
            cases[(r['repo'], r['number'], r['pr_id'])].append(r)
    out = ['# C2: restoration cases for reading', '',
           'One section per merged agent pull request whose changed expected value a later commit restored.', '']
    for (repo, number, pr_id), rs in sorted(cases.items()):
        pr = gh(f'repos/{repo}/pulls/{number}')
        pr_files = gh(f'repos/{repo}/pulls/{number}/files?per_page=100')
        pr_src = sorted(f['filename'] for f in pr_files if isinstance(pr_files, list) and not is_test(f['filename'])) \
            if isinstance(pr_files, list) else []
        out += [f"## {repo}#{number} ({rs[0]['agent']}), merged {rs[0]['merged_at'][:10]}", '',
                f"Title: {pr.get('title')}", '', f"PR: {rs[0]['url']}", '',
                'Body (start):', '', '```', (pr.get('body') or '')[:1200], '```', '',
                'Non-test files changed by the pull request: ' + (', '.join(pr_src[:12]) or 'none'), '']
        for sha in sorted({r['fate_sha'] for r in rs}):
            c = gh(f'repos/{repo}/commits/{sha}')
            files = [f['filename'] for f in c.get('files', [])]
            src = [f for f in files if not is_test(f)]
            author = (c.get('author') or {}).get('login') or c['commit']['author']['name']
            out += [f"Restoring commit {sha[:10]} on {c['commit']['committer']['date'][:10]} by {author}:", '',
                    '```', c['commit']['message'][:800], '```', '',
                    f"Files: {len(files)} ({len(src)} non-test); non-test files shared with the pull request: "
                    f"{', '.join(sorted(set(src) & set(pr_src))) or 'none'}", '']
        out += ['Restored lines:', '']
        seen = set()
        for r in rs:
            key = (r['removed'], r['added'])
            if key in seen:
                continue
            seen.add(key)
            out.append(f"- `{r['file']}`: agent `{r['added'][:110]}`, restored `{r['removed'][:110]}`")
        out += ['', 'Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER', '']
    (ROOT / 'review' / 'out' / 'c2_restorations.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'{len(cases)} cases written')


if __name__ == '__main__':
    main()
