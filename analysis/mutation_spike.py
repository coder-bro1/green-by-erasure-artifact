"""Two-program feasibility check for mutation analysis with Cosmic Ray (Phase 2 decision Q5).

For one HumanEvalFix pair and one version (fixed or buggy) this script:
1. pools every distinct test of that pair from the Phase 1 runs (generated tests and the final
   P1 to P4 versions, both conditions, all models), one file per test;
2. records each test's outcome on the unmutated program (baseline) and per-test branch coverage
   (coverage.py dynamic contexts);
3. lets Cosmic Ray enumerate the mutants (`cosmic-ray init` and `dump`), applies each one to a fresh
   copy (`cosmic-ray apply`), and runs all tests once per mutant, giving a per-test kill matrix.

A mutant is killed by a test only if that test passed on the unmutated program and fails, errors or
times out on the mutant. Tests that fail at baseline never count as kills. Any policy's mutation score
is then computed offline from the matrix, so every policy is scored on the same mutants.

Resumable: each mutant's result is written to its own file and skipped when present.
Usage: python analysis/mutation_spike.py --pair Python/11 --version fixed
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import download, program  # noqa: E402

RUNS = ['phase1_pilot', 'phase1_qwen35_pilot_r2', 'phase1_gemma4_pilot']
PY = sys.executable


def pooled_tests(pair_id):
    number = pair_id.split('/')[1]
    tests = {}
    for run in RUNS:
        for unit in sorted((ROOT / 'runs' / run / 'units').glob(f'HumanEvalFix-{number}__*')):
            generated = json.loads((unit / 'generated.json').read_text(encoding='utf-8'))
            sources = [(generated['prelude'], t['source']) for t in generated['tests']]
            for policy in ('P1', 'P2', 'P3', 'P4'):
                path = unit / f'policy_{policy}.json'
                if path.exists():
                    for t in json.loads(path.read_text(encoding='utf-8'))['tests']:
                        if t['final_status'] in ('KEPT', 'QUARANTINED'):
                            sources.append((t['prelude'], t['source']))
            for prelude, source in sources:
                text = prelude + '\n\n' + source + '\n'
                tests.setdefault(hashlib.sha256(text.encode()).hexdigest()[:16], text)
    return tests


def run_pytest(workdir, files, timeout):
    """Run the given test files once; return {file: 'PASS' | 'FAIL'} or None on time-out."""
    report = workdir / 'report.xml'
    report.unlink(missing_ok=True)
    try:
        subprocess.run([PY, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', f'--junitxml={report}', *files],
                       cwd=workdir, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    # A file passes only if it has at least one test case and none of its cases fails or errors;
    # a file that fails to collect has no passing case and counts as failing.
    passed, failed = set(), set()
    if report.exists():
        for case in ET.parse(report).iter('testcase'):
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
    # Whole-suite time-out (for example an infinite loop): run each test alone with its own limit.
    single = {}
    for f in files:
        r = run_pytest(workdir, [f], single_timeout)
        single[f] = 'TIMEOUT' if r is None else r[f]
    return single, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pair', required=True)
    ap.add_argument('--version', choices=('fixed', 'buggy'), required=True)
    args = ap.parse_args()
    rows = {r['task_id']: r for r in download()[0]}
    row = rows[args.pair]
    out = ROOT / '.scratch' / 'mutation_spike' / args.pair.replace('/', '_') / args.version
    out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    pristine = out / 'pristine'
    if not pristine.exists():
        (pristine / 'tests').mkdir(parents=True)
        (pristine / 'solution.py').write_text(program(row, args.version), encoding='utf-8')
        for key, text in pooled_tests(args.pair).items():
            (pristine / 'tests' / f'test_{key}.py').write_text(text, encoding='utf-8')
    files = sorted(f'tests/{p.name}' for p in (pristine / 'tests').glob('test_*.py'))

    # Baseline outcomes and per-test branch coverage on the unmutated program.
    baseline_path = out / 'baseline.json'
    if not baseline_path.exists():
        t0 = time.monotonic()
        # Two baseline runs; a test whose outcome differs between them is flaky and never green.
        first, fallback1 = outcomes(pristine, files)
        second, fallback2 = outcomes(pristine, files)
        base = {f: first[f] if first[f] == second[f] else 'FLAKY' for f in files}
        cov_t0 = time.monotonic()
        (pristine / '.coveragerc').write_text('[run]\nbranch = True\ninclude = solution.py\ndynamic_context = test_function\n',
                                              encoding='utf-8')
        # Coverage only for tests that finish at baseline; a test that times out there is red anyway.
        finishing = [f for f in files if base[f] in ('PASS', 'FAIL')]
        coverage_status = 'ok'
        try:
            subprocess.run([PY, '-m', 'coverage', 'run', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *finishing],
                           cwd=pristine, capture_output=True, text=True, timeout=300)
            subprocess.run([PY, '-m', 'coverage', 'json', '--show-contexts', '-o', 'coverage.json'],
                           cwd=pristine, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            coverage_status = 'timeout'
        baseline_path.write_text(json.dumps({'outcomes': base, 'seconds': cov_t0 - t0,
                                             'per_test_fallback': [fallback1, fallback2],
                                             'coverage_status': coverage_status,
                                             'coverage_seconds': time.monotonic() - cov_t0}, indent=1))
    baseline = json.loads(baseline_path.read_text())

    # Mutants, enumerated by Cosmic Ray.
    items_path = out / 'mutants.json'
    if not items_path.exists():
        (out / 'cr.toml').write_text(
            '[cosmic-ray]\nmodule-path = "solution.py"\ntimeout = 30.0\nexcluded-modules = []\n'
            'test-command = "python -m pytest -q tests"\n[cosmic-ray.distributor]\nname = "local"\n', encoding='utf-8')
        shutil.copy(pristine / 'solution.py', out / 'solution.py')
        subprocess.run([str(Path(PY).with_name('cosmic-ray.exe')), 'init', 'cr.toml', 'session.sqlite', '--force'],
                       cwd=out, check=True, capture_output=True, text=True)
        dump = subprocess.run([str(Path(PY).with_name('cosmic-ray.exe')), 'dump', 'session.sqlite'],
                              cwd=out, check=True, capture_output=True, text=True).stdout
        items = []
        for line in dump.splitlines():
            work_item = json.loads(line)[0]
            for m in work_item['mutations']:
                items.append({'job_id': work_item['job_id'], 'operator': m['operator_name'],
                              'occurrence': m['occurrence'], 'start': m['start_pos'], 'end': m['end_pos']})
        items_path.write_text(json.dumps(items, indent=1))
    items = json.loads(items_path.read_text())

    green = [f for f in files if baseline['outcomes'].get(f) == 'PASS']
    results_dir = out / 'mutants'
    results_dir.mkdir(exist_ok=True)
    for i, m in enumerate(items, 1):
        target = results_dir / f"{m['job_id']}.json"
        if target.exists():
            continue
        work = out / 'work'
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(pristine, work, ignore=shutil.ignore_patterns('.coverage*', 'coverage.json', 'report.xml'))
        t0 = time.monotonic()
        subprocess.run([str(Path(PY).with_name('cosmic-ray.exe')), 'apply', 'solution.py', m['operator'], str(m['occurrence'])],
                       cwd=work, check=True, capture_output=True, text=True)
        mutated = (work / 'solution.py').read_text(encoding='utf-8')
        res, fallback = outcomes(work, green) if green else ({}, False)
        killed = sorted(f for f, o in res.items() if o != 'PASS')
        target.write_text(json.dumps({**m, 'killed_by': killed, 'per_test_fallback': fallback,
                                      'seconds': time.monotonic() - t0,
                                      'mutant_sha256': hashlib.sha256(mutated.encode()).hexdigest()}))
        print(f'\r{args.pair} {args.version}: mutant {i}/{len(items)}', end='', flush=True)
    print()
    done = [json.loads(p.read_text()) for p in results_dir.glob('*.json')]
    status = baseline['outcomes'].values()
    summary = {'pair': args.pair, 'version': args.version, 'tests': len(files), 'green_tests': len(green),
               'baseline_timeouts': sum(o == 'TIMEOUT' for o in status), 'baseline_flaky': sum(o == 'FLAKY' for o in status),
               'baseline_per_test_fallback': baseline.get('per_test_fallback'),
               'coverage_status': baseline.get('coverage_status', 'ok'),
               'mutants': len(items), 'killed_by_any_green_test': sum(bool(d['killed_by']) for d in done),
               'per_test_fallbacks': sum(d['per_test_fallback'] for d in done),
               'mutant_seconds_total': round(sum(d['seconds'] for d in done), 1),
               'mutant_seconds_mean': round(sum(d['seconds'] for d in done) / max(len(done), 1), 2),
               'baseline_seconds': round(baseline['seconds'], 1), 'coverage_seconds': round(baseline['coverage_seconds'], 1),
               'wall_seconds_this_call': round(time.monotonic() - started, 1)}
    (out / 'summary.json').write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
