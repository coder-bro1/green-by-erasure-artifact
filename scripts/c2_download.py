"""C2: download the AIDev v4 tables we use (docs/C2_PLAN.md) into data/c2, verified by SHA-256.

Source: Hugging Face dataset hao-li/AIDev at tag v4 (CC-BY-4.0). The expected SHA-256 of each file is the
Git LFS object id that the Hugging Face API lists for the tag; the list is saved as data/c2/manifest.json.
Downloads go to <name>.part and are renamed only after the hash matches; a finished file is skipped on a
rerun. Standard library only. Usage: python scripts/c2_download.py
"""
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'c2'
REPO, TAG = 'hao-li/AIDev', 'v4'
FILES = ['repository.parquet', 'pull_request.parquet', 'pr_commits.parquet', 'pr_reviews.parquet',
         'pr_review_comments.parquet', 'pr_comments.parquet', 'pr_commit_details.parquet', 'README.md']


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(f'https://huggingface.co/api/datasets/{REPO}/tree/{TAG}?recursive=true', timeout=60) as r:
        tree = {f['path']: f for f in json.load(r) if f['type'] == 'file'}
    manifest = {'source': f'https://huggingface.co/datasets/{REPO}', 'tag': TAG, 'licence': 'CC-BY-4.0',
                'files': {name: {'size': tree[name]['size'], 'sha256': (tree[name].get('lfs') or {}).get('oid')}
                          for name in FILES}}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1), encoding='utf-8')
    for name in FILES:
        meta = manifest['files'][name]
        target = OUT / name
        if target.exists() and (meta['sha256'] is None or sha256(target) == meta['sha256']):
            print(f'{name}: already here, verified', flush=True)
            continue
        part = target.with_suffix(target.suffix + '.part')
        url = f'https://huggingface.co/datasets/{REPO}/resolve/{TAG}/{name}'
        t0, done = time.monotonic(), 0
        with urllib.request.urlopen(url, timeout=120) as r, open(part, 'wb') as fh:
            while chunk := r.read(1 << 20):
                fh.write(chunk)
                done += len(chunk)
                if done % (50 << 20) < (1 << 20):
                    rate = done / max(1e-6, time.monotonic() - t0) / 1e6
                    print(f'{name}: {done / 1e6:,.0f} of {meta["size"] / 1e6:,.0f} MB ({rate:.1f} MB/s)', flush=True)
        if meta['sha256'] and sha256(part) != meta['sha256']:
            print(f'{name}: SHA-256 MISMATCH, kept as {part.name}', flush=True)
            sys.exit(1)
        part.replace(target)
        print(f'{name}: done, {done / 1e6:,.1f} MB, verified', flush=True)
    print('All files downloaded and verified.', flush=True)


if __name__ == '__main__':
    main()
