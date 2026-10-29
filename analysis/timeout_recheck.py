"""P2-R1: re-execute every test whose evaluation timed out, with a 30 s limit, on an idle machine.

During the runs, evaluation executions had a 5 s limit; CPU load from other work occasionally pushed healthy
tests over it (for example 10 of 12,724 rechecked executions in the Gemma 4 run). For every evaluated test
(GEN and the final version under each policy) with a TIMEOUT in any of its four executions (two per version),
this script runs the same prelude and source again, twice per version, with a 30 s limit, and relabels it with
the harness's own rule (gbe.evaluate.label; FLAKY when the two runs disagree). A test that still times out
at 30 s keeps TIMEOUT (for example the buggy version of HumanEvalFix 10, which loops forever).

Outputs per run: runs/<run>/timeout_recheck.json (every rechecked test with old and new outcomes) and
runs/<run>/tests_rechecked.csv (tests.csv with corrected outcome_fixed, outcome_buggy, label, gen_label and
fate). tests.csv itself is never changed.

  python analysis/timeout_recheck.py --count            how many tests per run would be rechecked
  python analysis/timeout_recheck.py run_id [run_id ...] recheck (resumable; idle machine only)
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import all_tasks, program  # noqa: E402
from gbe.evaluate import fate, label  # noqa: E402
from gbe.execute import execute  # noqa: E402
from gbe.util import read_json, write_json  # noqa: E402

RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code', 'phase2_qwen25_spec', 'phase2_qwen25_seed1',
        'phase2_qwen25_seed2', 'phase2_qwen25_seed3', 'phase2_qwen25_disguised', 'phase2_qwen35_disguised',
        'phase2_gemma4_disguised', 'phase2_qwen25_natural']
LIMIT = 30


def timed_out(evidence):
    return {key: ex for key, ex in evidence.items()
            if any(e['outcome'] == 'TIMEOUT' for runs in ex['executions'].values() for e in runs)}


def source_of(unit, key):
    stage, test_id = key.split('/', 1)
    i = int(test_id.rsplit('/t', 1)[1])
    if stage == 'GEN':
        suite = read_json(unit / 'generated.json')
        return suite['prelude'], suite['tests'][i]['source']
    test = read_json(unit / f'policy_{stage}.json')['tests'][i]
    return test['prelude'], test['source']


def count():
    total = 0
    for run in RUNS:
        if not (ROOT / 'runs' / run / 'units').exists():
            continue
        units = sorted((ROOT / 'runs' / run / 'units').iterdir())
        n = sum(len(timed_out(read_json(u / 'evaluation_evidence.json'))) for u in units
                if (u / 'evaluation_evidence.json').exists())
        total += n
        print(f'{run}: {n} evaluated tests with a TIMEOUT execution')
    print(f'total: {total}')


_TASKS = None


def recheck_one(job):
    """One test, in a worker process: two executions per version with the 30 s limit."""
    global _TASKS
    if _TASKS is None:
        _TASKS = {t['task_id']: t for t in all_tasks()[0]}
    full, unit, key, pair_id, old = job
    task = _TASKS[pair_id]
    prelude, source = source_of(Path(unit), key)
    # Stage C tasks run in their own environments; the runtime's limit is replaced by the recheck limit.
    runtimes = {c: dict(task['runtime'][c], timeout=LIMIT) for c in ('fixed', 'buggy')} if 'runtime' in task else {}
    new = {c: [execute(program(task, c), prelude, source, timeout=LIMIT, support=task.get('support'),
                       runtime=runtimes.get(c))['outcome']
               for _ in range(2)] for c in ('fixed', 'buggy')}
    flaky = any(v[0] != v[1] for v in new.values())
    return full, {'old': old, 'new': new, 'label': 'FLAKY' if flaky else label(new['fixed'][0], new['buggy'][0])}


def recheck(run, workers):
    folder = ROOT / 'runs' / run
    out_path = folder / 'timeout_recheck.json'
    done = read_json(out_path) if out_path.exists() else {}
    with open(folder / 'tests.csv', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    pair_of = {r['unit_id']: r['pair_id'] for r in rows}
    units = sorted(u for u in (folder / 'units').iterdir() if (u / 'evaluation_evidence.json').exists())
    jobs = []
    for unit in units:
        for key, ex in timed_out(read_json(unit / 'evaluation_evidence.json')).items():
            full = unit.name + '|' + key
            if full not in done:
                jobs.append((full, str(unit), key, pair_of[unit.name],
                             {c: [e['outcome'] for e in runs] for c, runs in ex['executions'].items()}))
    from concurrent.futures import ProcessPoolExecutor, as_completed
    sys.path.insert(0, str(ROOT / 'analysis'))
    from memlimit import cap  # each worker and its pytest children capped (runaway tests, 14 October)
    with ProcessPoolExecutor(max_workers=workers, initializer=cap) as pool:
        for n, future in enumerate(as_completed([pool.submit(recheck_one, j) for j in jobs])):
            full, result = future.result()
            done[full] = result
            write_json(out_path, done)
            if n % 20 == 0:
                print(f'{run}: {n + 1}/{len(jobs)} rechecked', flush=True)
    # Corrected table: replace the evaluation of rechecked tests, then the generation label of every row of
    # the same test, then the fate.
    fixes = {}
    for full, d in done.items():
        unit, key = full.split('|', 1)
        stage, test_id = key.split('/', 1)
        fixes[(stage, test_id)] = d
    gen_new = {test_id: d['label'] for (stage, test_id), d in fixes.items() if stage == 'GEN'}
    changed = 0
    for r in rows:
        d = fixes.get((r['stage'], r['test_id']))
        if d:
            before = r['label']
            r['outcome_fixed'], r['outcome_buggy'], r['label'] = d['new']['fixed'][0], d['new']['buggy'][0], d['label']
            changed += before != r['label']
            if r['stage'] == 'GEN':
                r['gen_label'] = d['label']
        if r['stage'] != 'GEN' and r['test_id'] in gen_new:
            r['gen_label'] = gen_new[r['test_id']]
        if r['stage'] != 'GEN' and r['condition'] == 'buggy':
            r['fate'] = fate(r['gen_label'], r['final_status'], r['label'])  # the harness's own rule
    with open(folder / 'tests_rechecked.csv', 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'{run}: {len(done)} tests rechecked, {changed} labels changed')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('runs', nargs='*')
    ap.add_argument('--count', action='store_true')
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    if a.count:
        count()
    else:
        for run in a.runs or RUNS:
            if (ROOT / 'runs' / run / 'tests.csv').exists():  # runs not finished yet are skipped
                recheck(run, a.workers)

