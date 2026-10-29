"""C2 stage B-2: commit-level inspection of the possible-erasure cases before any executable replay.

For every case with final label E (review/c2_labels/c2_final_labels.csv), prints from the GitHub API (read only,
cached by c2_step3.gh): the commit message of each commit that changed an expected value, and the test-file hunk
around the changed assert, so a reader can see whether the change is a formatting artefact, a test-infrastructure
change or a behaviour change. Writes review/out/c2_inspection.md. Runs in .venv-c2.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c2_inspect.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from c2_step3 import gh  # noqa: E402


def hunk_around(patch, needles, width=8):
    lines = (patch or '').splitlines()
    hits = [i for i, l in enumerate(lines) if any(n and n in l for n in needles)]
    if not hits:
        return '(changed lines not found in the patch; the patch may be truncated)'
    lo, hi = max(0, min(hits) - width), min(len(lines), max(hits) + width + 1)
    return '\n'.join(lines[lo:hi])


def main():
    fl = pd.read_csv(ROOT / 'review' / 'c2_labels' / 'c2_final_labels.csv')
    cases = fl[fl.final_why == 'E']
    pairs = [json.loads(line) for line in open(ROOT / 'runs' / 'c2' / 'pairs.jsonl', encoding='utf-8')]
    out = ['# C2: commit-level inspection of the 13 possible erasures', '',
           'Read-only GitHub API. For each case: the commits that changed an expected value, their message, and the',
           'test-file hunk around the change.', '']
    for r in cases.itertuples():
        repo = '/'.join(r.link.split('/')[3:5])
        num = int(r.link.split('/')[-1])
        ps = [p for p in pairs if p['repo'] == repo and p['number'] == num and p['mode'] == 'EXPECTED_CHANGED']
        out += [f'## {r.case}: {repo}#{num} ({r.agent}, merged {r.merged})', '', f'{r.title}', '']
        by_commit = defaultdict(list)
        for p in ps:
            by_commit[(p['sha'], p['file'])].append(p)
        for (sha, file), group in list(by_commit.items())[:3]:
            c = gh(f'repos/{repo}/commits/{sha}')
            msg = (c.get('commit', {}).get('message', '') if isinstance(c, dict) else '').strip().splitlines()
            patch = next((f.get('patch') for f in (c.get('files', []) if isinstance(c, dict) else []) if f.get('filename') == file), '')
            needles = [g['removed'].strip()[:60] for g in group] + [g['added'].strip()[:60] for g in group]
            out += [f'Commit {sha[:10]}: {msg[0] if msg else "(no message)"}', '', f'File {file}:', '', '```diff',
                    hunk_around(patch, needles), '```', '']
    (ROOT / 'review' / 'out' / 'c2_inspection.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'{len(cases)} cases written to review/out/c2_inspection.md')


if __name__ == '__main__':
    main()
