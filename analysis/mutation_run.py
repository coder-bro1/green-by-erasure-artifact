"""M1: coverage and mutation analysis of every Phase 2 test (docs/PHASE2_SPEC.md section 6).

For every program version (fixed and buggy) of every pair used in the Phase 2 runs:
1. pool every distinct test of that pair from all runs (generated tests and final versions under each policy,
   KEPT or QUARANTINED, both conditions, all models, inputs and seeds), one file per test, keyed by the hash
   of its text; the index of which (run, unit, stage, test) uses which file goes to the result;
2. baseline: run all pooled tests twice on the unmutated version (a test whose outcome differs is FLAKY and
   never green), then per-test line and branch coverage (coverage.py dynamic contexts) for tests that finish;
3. let Cosmic Ray enumerate the mutants, apply each to a fresh copy and run the green tests once: a mutant is
   killed by a test that passed at baseline and fails, errors or times out on it (whole-run limit 60 s, then
   each test alone with 10 s).
The per-test kill matrix and coverage are written to runs/phase2_mutation/results/<pair>__<version>.json; any
suite's mutation score and coverage are computed offline from them. Working folders live under
.scratch/mutation (not in git). Resumable per mutant and per version; versions run in parallel worker processes
at below-normal priority. Idle machine only (the same time-out sensitivity as the evaluation).

  python analysis/mutation_run.py --plan                 count pairs, versions and pooled tests
  python analysis/mutation_run.py --only Python/11       run one pair (both versions)
  python analysis/mutation_run.py --workers 6            run everything
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import all_tasks, benchmark_name, program  # noqa: E402
from gbe.util import now, read_json, write_json  # noqa: E402

RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code', 'phase2_qwen25_spec', 'phase2_qwen25_seed1',
        'phase2_qwen25_seed2', 'phase2_qwen25_seed3', 'phase2_qwen25_disguised', 'phase2_qwen35_disguised',
        'phase2_gemma4_disguised', 'phase2_qwen25_natural']
PY = sys.executable
CR = str(Path(PY).with_name('cosmic-ray.exe'))
WORK = ROOT / '.scratch' / 'mutation'
OUT = ROOT / 'runs' / 'phase2_mutation'
BELOW_NORMAL = 0x4000 if os.name == 'nt' else 0


def unit_prefix(task):
    return f"{benchmark_name(task)}-{task['task_id'].split('/')[-1]}__"


def pooled_tests(task):
    """{key: text} and {key: [[run, unit, stage, index], ...]} over every Phase 2 run."""
    tests, index = {}, {}
    for run in RUNS:
        units = ROOT / 'runs' / run / 'units'
        if not units.exists():
            continue
        for unit in sorted(units.glob(unit_prefix(task) + '*')):
            if not (unit / 'generated.json').exists():
                continue
            generated = read_json(unit / 'generated.json')
            sources = [('GEN', i, generated['prelude'], t['source']) for i, t in enumerate(generated['tests'])]
            for policy in ('P1', 'P2', 'P3', 'P4'):
                path = unit / f'policy_{policy}.json'
                if path.exists():
                    for i, t in enumerate(read_json(path)['tests']):
                        if t['final_status'] in ('KEPT', 'QUARANTINED'):
                            sources.append((policy, i, t['prelude'], t['source']))
            for stage, i, prelude, source in sources:
                text = prelude + '\n\n' + source + '\n'
                key = hashlib.sha256(text.encode()).hexdigest()[:16]
                tests.setdefault(key, text)
                index.setdefault(key, []).append([run, unit.name, stage, i])
    return tests, index


def run_limited(command, cwd, timeout):
    """Run a command with a hard wall limit and kill its whole process tree on time-out. On Windows the venv's
    python.exe is a launcher that starts the real interpreter as a child; killing only the launcher (what
    subprocess.run does) left infinite tests running for hours and blocked the pipes (15 October), as
    gbe.execute already notes. Returns True if the command finished in time."""
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=BELOW_NORMAL)
    try:
        process.wait(timeout=timeout)
        return True
    except subprocess.TimeoutExpired:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        process.kill()
        process.wait()
        return False


def run_pytest(workdir, files, timeout):
    report = workdir / 'report.xml'
    report.unlink(missing_ok=True)
    if not run_limited([PY, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', f'--junitxml={report}', *files],
                       workdir, timeout):
        return None
    passed, failed = set(), set()
    if report.exists():
        try:
            cases = list(ET.parse(report).iter('testcase'))
        except ET.ParseError:
            # A pytest process stopped while writing its report (for example by the 2 GB memory cap, when a
            # mutant loops and allocates): treated like a time-out, so each test is rerun alone (15 October).
            return None
        for case in cases:
            name = 'tests/' + case.get('classname', '').split('.')[-1] + '.py'
            if any(child.tag in ('failure', 'error') for child in case):
                failed.add(name)
            elif not any(child.tag == 'skipped' for child in case):
                passed.add(name)
    return {f: 'PASS' if f in passed and f not in failed else 'FAIL' for f in files}


def outcomes(workdir, files, timeout=60, single_timeout=10):
    result = run_pytest(workdir, files, timeout)
    if result is not None:
        return result, False
    single = {}
    for f in files:
        r = run_pytest(workdir, [f], single_timeout)
        single[f] = 'TIMEOUT' if r is None else r[f]
    return single, True


def per_test_coverage(pristine):
    """{test file: {'lines': [...], 'arcs': [[a, b], ...]}} from coverage.py dynamic contexts."""
    import coverage
    data = coverage.CoverageData(basename=str(pristine / '.coverage'))
    data.read()
    target = next((f for f in data.measured_files() if f.endswith('solution.py')), None)
    result = {}
    if not target:
        return result
    for context in data.measured_contexts():
        if not context:
            continue
        module = context.split('.')[0]
        data.set_query_contexts([context])
        entry = result.setdefault(f'tests/{module}.py', {'lines': set(), 'arcs': set()})
        entry['lines'] |= set(data.lines(target) or [])
        entry['arcs'] |= {tuple(a) for a in (data.arcs(target) or [])}
    return {k: {'lines': sorted(v['lines']), 'arcs': sorted(list(a) for a in v['arcs'])} for k, v in result.items()}


def run_version(task, version):
    key = task['task_id'].replace('/', '_')
    target = OUT / 'results' / f'{key}__{version}.json'
    if target.exists():
        return str(target), 'done before'
    work = WORK / key / version
    work.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    tests, index = pooled_tests(task)
    pristine = work / 'pristine'
    if not (pristine / 'pool.json').exists():
        shutil.rmtree(pristine, ignore_errors=True)
        (pristine / 'tests').mkdir(parents=True)
        (pristine / 'solution.py').write_text(program(task, version), encoding='utf-8')
        for name, text in (task.get('support') or {}).items():
            (pristine / name).write_text(text, encoding='utf-8')
        for k, text in tests.items():
            (pristine / 'tests' / f'test_{k}.py').write_text(text, encoding='utf-8')
        write_json(pristine / 'pool.json', sorted(tests))
    files = sorted(f'tests/test_{k}.py' for k in read_json(pristine / 'pool.json'))
    baseline_path = work / 'baseline.json'
    if not baseline_path.exists():
        first, fb1 = outcomes(pristine, files)
        second, fb2 = outcomes(pristine, files)
        base = {f: first[f] if first[f] == second[f] else 'FLAKY' for f in files}
        (pristine / '.coveragerc').write_text('[run]\nbranch = True\ninclude = solution.py\ndynamic_context = test_function\n',
                                              encoding='utf-8')
        finishing = [f for f in files if base[f] in ('PASS', 'FAIL')]
        status = 'ok'
        if run_limited([PY, '-m', 'coverage', 'run', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *finishing],
                       pristine, 600):
            cov = per_test_coverage(pristine)
        else:
            status, cov = 'timeout', {}
        write_json(baseline_path, {'outcomes': base, 'fallback': [fb1, fb2], 'coverage_status': status, 'coverage': cov})
    baseline = read_json(baseline_path)
    items_path = work / 'mutants.json'
    if not items_path.exists():
        (work / 'cr.toml').write_text(
            '[cosmic-ray]\nmodule-path = "solution.py"\ntimeout = 30.0\nexcluded-modules = []\n'
            'test-command = "python -m pytest -q tests"\n[cosmic-ray.distributor]\nname = "local"\n', encoding='utf-8')
        shutil.copy(pristine / 'solution.py', work / 'solution.py')
        subprocess.run([CR, 'init', 'cr.toml', 'session.sqlite', '--force'], cwd=work, check=True, capture_output=True,
                       text=True, creationflags=BELOW_NORMAL)
        dump = subprocess.run([CR, 'dump', 'session.sqlite'], cwd=work, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace',
                              creationflags=BELOW_NORMAL).stdout
        items = []
        for line in dump.splitlines():
            item = json.loads(line)[0]
            for m in item['mutations']:
                items.append({'job_id': item['job_id'], 'operator': m['operator_name'], 'occurrence': m['occurrence'],
                              'start': m['start_pos'], 'end': m['end_pos']})
        write_json(items_path, items)
    items = read_json(items_path)
    green = [f for f in files if baseline['outcomes'].get(f) == 'PASS']
    results_dir = work / 'mutants'
    results_dir.mkdir(exist_ok=True)
    for m in items:
        path = results_dir / f"{m['job_id']}.json"
        if path.exists():
            continue
        # A fresh folder per mutant: on Windows a test killed at its time limit can keep files locked for a
        # while, so emptying one shared folder failed (FileExistsError on copytree) and stopped three versions
        # on 15 October. Old folders are removed best effort.
        for old in work.glob('work*'):
            shutil.rmtree(old, ignore_errors=True)
        scratch = work / f"work_{m['job_id']}"
        shutil.rmtree(scratch, ignore_errors=True)
        shutil.copytree(pristine, scratch, ignore=shutil.ignore_patterns('.coverage*', 'report.xml'))
        t0 = time.monotonic()
        subprocess.run([CR, 'apply', 'solution.py', m['operator'], str(m['occurrence'])], cwd=scratch, check=True,
                       capture_output=True, text=True, encoding='utf-8', errors='replace', creationflags=BELOW_NORMAL)
        mutated = (scratch / 'solution.py').read_text(encoding='utf-8')
        res, fallback = outcomes(scratch, green) if green else ({}, False)
        write_json(path, {**m, 'killed_by': sorted(f for f, o in res.items() if o != 'PASS'), 'fallback': fallback,
                          'seconds': round(time.monotonic() - t0, 2),
                          'mutant_sha256': hashlib.sha256(mutated.encode()).hexdigest()})
    mutants = [read_json(results_dir / f"{m['job_id']}.json") for m in items]
    write_json(target, {'pair_id': task['task_id'], 'benchmark': benchmark_name(task), 'version': version,
                        'tests': {f'tests/test_{k}.py': index[k] for k in read_json(pristine / 'pool.json')},
                        'baseline': baseline['outcomes'], 'baseline_fallback': baseline['fallback'],
                        'coverage_status': baseline['coverage_status'], 'coverage': baseline['coverage'],
                        'mutants': [{k: m[k] for k in ('job_id', 'operator', 'occurrence', 'start', 'end', 'killed_by',
                                                       'fallback', 'seconds', 'mutant_sha256')} for m in mutants],
                        'seconds': round(time.monotonic() - started, 1), 'finished': now()})
    return str(target), f'{len(items)} mutants, {len(green)} of {len(files)} tests green'


def tasks_in_runs():
    used = set()
    for run in RUNS:
        p = ROOT / 'runs' / run / 'pairs.json'
        if p.exists():
            used |= {x['pair_id'] for x in read_json(p)}
    return [t for t in all_tasks()[0] if t['task_id'] in used]


def job(args):
    sys.path.insert(0, str(ROOT / 'analysis'))
    from memlimit import cap
    cap()  # this worker and its pytest children are memory-capped (runaway tests, 14 October)
    task_id, version = args
    task = {t['task_id']: t for t in all_tasks()[0]}[task_id]
    return task_id, version, run_version(task, version)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    tasks = tasks_in_runs()
    if a.only:
        tasks = [t for t in tasks if t['task_id'] in a.only]
    if a.plan:
        sizes = {t['task_id']: len(pooled_tests(t)[0]) for t in tasks}
        print(f'{len(tasks)} pairs, {2 * len(tasks)} versions, {sum(sizes.values())} pooled tests per version set '
              f'(mean {sum(sizes.values()) / max(1, len(sizes)):.0f}, max {max(sizes.values())})')
        return
    jobs = [(t['task_id'], v) for t in tasks for v in ('fixed', 'buggy')]
    OUT.mkdir(parents=True, exist_ok=True)
    from concurrent.futures import ProcessPoolExecutor, as_completed
    done = 0
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for future in as_completed([pool.submit(job, j) for j in jobs]):
            task_id, version, (path, note) = future.result()
            done += 1
            write_json(OUT / 'progress.json', {'done': done, 'total': len(jobs), 'percent': round(100 * done / len(jobs), 1),
                                               'last': f'{task_id} {version}: {note}', 'updated': now()})
            print(f'{done}/{len(jobs)} {task_id} {version}: {note}', flush=True)


if __name__ == '__main__':
    if os.name == 'nt':
        import ctypes
        k32 = ctypes.windll.kernel32
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        k32.SetPriorityClass(k32.GetCurrentProcess(), BELOW_NORMAL)
    main()
