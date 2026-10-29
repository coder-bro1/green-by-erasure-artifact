"""Real repository bugs from BugsInPy as a benchmark (stage C, docs/C1_PROTOCOL.md).

The 30 eligible bugs, built by analysis/c1_build_tasks.py into data/c1/tasks.json and pinned by configs/c1.json.
Each task shows the changed function (with its module's imports and enclosing class headers) per version; tests
import it through a solution.py shim from the bug's own checkout and environment (gbe.execute runtime).
Step 3 evidence (developer test, twice per version) is in configs/c1_sanity.json. Empty until built.
"""
import hashlib
import json

from .util import ROOT, read_json

BENCHMARK = 'BugsInPy'


def load():
    pin = ROOT / 'configs' / 'c1.json'
    if not pin.exists():
        return []
    pinned = read_json(pin)
    path = ROOT / pinned['file']
    tasks = json.loads(path.read_text(encoding='utf-8'))
    if content_hash(tasks) != pinned['sha256']:
        raise ValueError('BugsInPy task file differs from the pinned hash')
    return list(tasks.values())


def content_hash(tasks):
    """SHA-256 of the tasks without their `runtime` entries, which hold this machine's environment and
    checkout paths and are rewritten when the file is exported or the environments are rebuilt."""
    content = {k: {f: v for f, v in t.items() if f != 'runtime'} for k, t in tasks.items()}
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
