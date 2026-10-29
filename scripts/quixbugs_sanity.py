"""Run QuixBugs' own pytest cases twice on each normalised version and write configs/quixbugs_sanity.json.

The runner refuses QuixBugs tasks whose normalised sources no longer match the hashes recorded here.
Usage: .venv\Scripts\python.exe scripts/quixbugs_sanity.py  (about 15 minutes; buggy versions that loop hit the 60 s limit)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from gbe import quixbugs  # noqa: E402
from gbe.benchmarks import program  # noqa: E402
from gbe.util import ROOT, digest, write_json  # noqa: E402

out = {}
for task in quixbugs.load():
    entry = {c: [quixbugs.sanity(task, c)[0] for _ in range(2)] for c in ('fixed', 'buggy')}
    entry['source_hashes'] = {c: digest(program(task, c)) for c in ('fixed', 'buggy')}
    out[task['task_id']] = entry
    print(task['task_id'], {k: v for k, v in entry.items() if k != 'source_hashes'}, flush=True)
write_json(ROOT / 'configs' / 'quixbugs_sanity.json', out)
