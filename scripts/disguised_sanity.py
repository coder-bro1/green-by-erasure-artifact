"""Pin the disguised task file and record its sanity evidence (S1, docs/PHASE2_SPEC.md 8.8).

Writes configs/disguised.json (path and sha256 of runs/d11/disguised_tasks.json) and
configs/disguised_sanity.json: HumanEval's own tests, called through name aliases, run twice on each
version with the harness executor, bound to the source hashes (the same shape as quixbugs_sanity.json).
A pair is usable when its fixed version passes and its buggy version fails both times.
Usage: python scripts/disguised_sanity.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import download, program  # noqa: E402
from gbe.execute import execute  # noqa: E402
from gbe.util import digest, write_json  # noqa: E402

FILE = 'runs/d11/disguised_tasks.json'


def main():
    data = (ROOT / FILE).read_bytes()
    write_json(ROOT / 'configs' / 'disguised.json', {
        'purpose': 'S1 contamination control: disguised HumanEvalFix pairs built by scripts/d11_disguise.py',
        'file': FILE, 'sha256': hashlib.sha256(data).hexdigest(),
        'verification': 'runs/d11/disguised_verification.json'})
    from gbe import disguised
    rows = {r['task_id']: r for r in download()[0]}
    raw = json.loads(data.decode('utf-8'))
    evidence = {}
    for task in disguised.load():
        prelude, test = disguised.hidden_parts(rows[task['original_pair_id']], raw[task['original_pair_id']])
        entry = {c: [execute(program(task, c), prelude, test, timeout=15)['outcome'] for _ in range(2)]
                 for c in ('fixed', 'buggy')}
        entry['source_hashes'] = {c: digest(program(task, c)) for c in ('fixed', 'buggy')}
        evidence[task['task_id']] = entry
        print(task['task_id'], entry['fixed'], entry['buggy'], flush=True)
    write_json(ROOT / 'configs' / 'disguised_sanity.json', evidence)
    usable = sum(all(o == 'PASS' for o in e['fixed']) and all(o != 'PASS' for o in e['buggy']) for e in evidence.values())
    print(f'{usable} of {len(evidence)} pairs usable')


if __name__ == '__main__':
    main()
