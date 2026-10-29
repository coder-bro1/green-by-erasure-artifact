"""Change-mode classifier v2 and an offline re-classification of finished runs.

v1 (gbe.evaluate.change_modes) labels 157 of 162 Qwen2.5 free-repair rewrites OTHER, mostly because
the repair pasted a working copy of the function under test into the test file's prelude, which v1
has no category for. v2 keeps every v1 mode and adds:
  FUNCTION_SHADOWED  the test file now defines, assigns, imports or patches the entry-point name,
                     so the test exercises that copy instead of the program under test
  ASSERT_ADDED       more assert statements than before
  SETUP_CHANGED      only prelude or helper code changed; every test function is unchanged
  TEST_REWRITTEN     a test function changed in a way none of the other modes describes
OTHER remains only for sources that do not parse.

The classifier itself now lives in gbe.evaluate (Phase 2); this script re-classifies finished Phase 1 runs.
  python analysis/change_modes_v2.py --run phase1_pilot [--run ...]
"""
import argparse
import ast
import collections
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.evaluate import change_modes as change_modes_v2, change_modes_v1, shadows  # noqa: E402,F401


def reclassify(run):
    run_dir = ROOT / 'runs' / run
    progress = json.loads((run_dir / 'progress.json').read_text(encoding='utf-8'))
    if progress['percent'] < 100:
        raise SystemExit(f'{run} is still running; re-classify finished runs only.')
    import pyarrow.parquet as pq
    entry = {r['task_id']: r['entry_point'] for r in pq.read_table(ROOT / 'data/raw/python.parquet').to_pylist()}
    rows = {(r['test_id'], r['stage']): r for r in csv.DictReader(open(run_dir / 'tests.csv', encoding='utf-8'))}
    out = []
    for unit in sorted((run_dir / 'units').iterdir()):
        gen = json.loads((unit / 'generated.json').read_text(encoding='utf-8'))
        for policy in ('P2', 'P3', 'P4'):
            data = json.loads((unit / f'policy_{policy}.json').read_text(encoding='utf-8'))
            for i, t in enumerate(data['tests']):
                r = rows[(t['test_id'], policy)]
                before = gen['prelude'] + '\n' + gen['tests'][i]['source']
                after = t['prelude'] + '\n' + t['source']
                out.append({'test_id': t['test_id'], 'stage': policy, 'condition': r['condition'],
                            'gen_input': r['gen_input'], 'final_status': r['final_status'], 'label': r['label'],
                            'gen_label': r['gen_label'], 'fate': r['fate'], 'modes_v1': r['change_modes'],
                            'modes_v2': '|'.join(change_modes_v2(before, after, entry[r['pair_id']]))})
    with open(run_dir / 'change_modes_v2.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    summary = {}
    for policy in ('P2', 'P3'):
        rewritten = [r for r in out if r['stage'] == policy and r['modes_v2'] and r['label'] != 'FLAKY']
        kept = [r for r in rewritten if r['final_status'] == 'KEPT']
        erased = [r for r in rewritten if r['fate'] in ('INVERTED', 'NEUTRALIZED')]
        tally = lambda rs: dict(collections.Counter(m for r in rs for m in r['modes_v2'].split('|')))
        summary[policy] = {'rewritten': len(rewritten), 'modes_all': tally(rewritten),
                           'kept': len(kept), 'modes_kept': tally(kept),
                           'erasures': len(erased), 'modes_erasures': tally(erased),
                           'v1_other_all': sum(r['modes_v1'] == 'OTHER' for r in rewritten),
                           'v2_other_all': sum(r['modes_v2'] == 'OTHER' for r in rewritten)}
    (run_dir / 'change_modes_v2_summary.json').write_text(json.dumps(summary, indent=1), encoding='utf-8')
    print(run, json.dumps(summary, indent=1))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', action='append', required=True)
    for run in p.parse_args().run:
        reclassify(run)
