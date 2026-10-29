"""Kill matrix for tests outside the Phase 2 mutation pool (S6 model-only overwrite), against the same mutants.

analysis/mutation_run.py pools every Phase 2 test per program version; rebuilding a pool to add a run would rerun
all of them. This script instead takes the final P2M tests of an S6 run (KEPT or QUARANTINED, from units generated
for that version), skips any test whose text is already in the version's pool (its kills are in
runs/phase2_mutation/results), and runs only the new ones: twice on the unmutated version for the baseline, then
once on each mutant recorded in the pool's result file. Each mutant is re-applied with Cosmic Ray and its source
hash checked against the recorded mutant_sha256, so the kills refer to the same mutants. Time limits, the kill
rule and the memory cap are those of mutation_run.py. Idle machine only.

Output per version: runs/<run>/mutation/<pair>__<version>.json with the test index (new and reused tests), the
baseline of the new tests and, per mutant, the new tests that kill it. Resumable per mutant.

  python analysis/mutation_extra.py --run s6_model_only_gemma4 [--only HumanEvalFix/0] [--workers 6]
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'analysis'))
import mutation_run as mr  # noqa: E402
from gbe.benchmarks import all_tasks, program  # noqa: E402
from gbe.util import now, read_json, write_json  # noqa: E402


def new_tests(run, task, version, pool):
    """{key: text} of P2M tests not in the pool, and {test file: [[run, unit, stage, index], ...]} for all."""
    tests, index = {}, {}
    for unit in sorted((ROOT / 'runs' / run / 'units').glob(mr.unit_prefix(task) + '*')):
        if f'__{version}__' not in unit.name or not (unit / 'policy_P2M.json').exists():
            continue
        for i, t in enumerate(read_json(unit / 'policy_P2M.json')['tests']):
            if t['final_status'] not in ('KEPT', 'QUARANTINED'):
                continue
            text = t['prelude'] + '\n\n' + t['source'] + '\n'
            key = hashlib.sha256(text.encode()).hexdigest()[:16]
            index.setdefault(f'tests/test_{key}.py', []).append([run, unit.name, 'P2M', i])
            if f'tests/test_{key}.py' not in pool:
                tests[key] = text
    return tests, index


def run_version(run, task, version):
    key = task['task_id'].replace('/', '_')
    target = ROOT / 'runs' / run / 'mutation' / f'{key}__{version}.json'
    if target.exists():
        return 'done before'
    main = read_json(mr.OUT / 'results' / f'{key}__{version}.json')
    tests, index = new_tests(run, task, version, main['tests'])
    started = time.monotonic()
    work = ROOT / '.scratch' / 'mutation_extra' / run / key / version
    pristine = work / 'pristine'
    if tests and not (pristine / 'pool.json').exists():
        shutil.rmtree(pristine, ignore_errors=True)
        (pristine / 'tests').mkdir(parents=True)
        (pristine / 'solution.py').write_text(program(task, version), encoding='utf-8')
        for name, text in (task.get('support') or {}).items():
            (pristine / name).write_text(text, encoding='utf-8')
        for k, text in tests.items():
            (pristine / 'tests' / f'test_{k}.py').write_text(text, encoding='utf-8')
        write_json(pristine / 'pool.json', sorted(tests))
    files = sorted(f'tests/test_{k}.py' for k in tests)
    baseline = {}
    if files:
        baseline_path = work / 'baseline.json'
        if not baseline_path.exists():
            first, _ = mr.outcomes(pristine, files)
            second, _ = mr.outcomes(pristine, files)
            write_json(baseline_path, {f: first[f] if first[f] == second[f] else 'FLAKY' for f in files})
        baseline = read_json(baseline_path)
    green = [f for f in files if baseline.get(f) == 'PASS']
    results_dir = work / 'mutants'
    results_dir.mkdir(parents=True, exist_ok=True)
    mutants = []
    for m in main['mutants']:
        path = results_dir / f"{m['job_id']}.json"
        if not path.exists():
            killed, matched, fallback = [], True, False
            if green:
                for old in work.glob('work*'):
                    shutil.rmtree(old, ignore_errors=True)
                scratch = work / f"work_{m['job_id']}"
                shutil.copytree(pristine, scratch, ignore=shutil.ignore_patterns('.coverage*', 'report.xml'))
                subprocess.run([mr.CR, 'apply', 'solution.py', m['operator'], str(m['occurrence'])], cwd=scratch,
                               check=True, capture_output=True, text=True, encoding='utf-8', errors='replace',
                               creationflags=mr.BELOW_NORMAL)
                mutated = (scratch / 'solution.py').read_text(encoding='utf-8')
                matched = hashlib.sha256(mutated.encode()).hexdigest() == m['mutant_sha256']
                res, fallback = mr.outcomes(scratch, green)
                killed = sorted(f for f, o in res.items() if o != 'PASS')
            write_json(path, {'job_id': m['job_id'], 'killed_by': killed, 'mutant_matches': matched,
                              'fallback': fallback})
        mutants.append(read_json(path))
    write_json(target, {'pair_id': task['task_id'], 'version': version, 'run': run, 'tests': index,
                        'new_tests': files, 'baseline': baseline, 'mutants': mutants,
                        'seconds': round(time.monotonic() - started, 1), 'finished': now()})
    return f'{len(main["mutants"])} mutants, {len(green)} of {len(files)} new tests green, {len(index) - len(files)} reused'


def job(args):
    from memlimit import cap
    cap()
    run, task_id, version = args
    task = {t['task_id']: t for t in all_tasks()[0]}[task_id]
    return task_id, version, run_version(run, task, version)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    source = read_json(ROOT / 'runs' / a.run / 'manifest.json')['source_run']
    pairs = [p['pair_id'] for p in read_json(ROOT / 'runs' / source / 'pairs.json')]
    if a.only:
        pairs = [p for p in pairs if p in a.only]
    jobs = [(a.run, p, v) for p in pairs for v in ('buggy', 'fixed')
            if (mr.OUT / 'results' / f"{p.replace('/', '_')}__{v}.json").exists()]
    (ROOT / 'runs' / a.run / 'mutation').mkdir(parents=True, exist_ok=True)
    from concurrent.futures import ProcessPoolExecutor, as_completed
    done = 0
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for future in as_completed([pool.submit(job, j) for j in jobs]):
            task_id, version, note = future.result()
            done += 1
            write_json(ROOT / 'runs' / a.run / 'mutation' / 'progress.json',
                       {'done': done, 'total': len(jobs), 'last': f'{task_id} {version}: {note}', 'updated': now()})
            print(f'{done}/{len(jobs)} {task_id} {version}: {note}', flush=True)


if __name__ == '__main__':
    main()
