"""RQ2 (visibility, formerly RQ3): coverage and mutation score of every suite beside the bug evidence it keeps.

Inputs: the per-version kill matrices and per-test coverage of analysis/mutation_run.py
(runs/phase2_mutation/results) and each run's per-test table after the time-out recheck (tests_rechecked.csv,
or tests.csv where no recheck file exists). Definitions follow docs/PHASE2_SPEC.md 6.3:
- a suite is a unit's generated tests (GEN) or its final tests under a policy (P1 to P4, KEPT and, for P4,
  QUARANTINED);
- only the suite's tests that pass at baseline on version V count for the mutation score ("green"); mutation
  score on V = mutants killed by a green test / all mutants of V; a version without mutants has no score;
- line coverage on V = lines of solution.py executed / executable lines (statement lines from the syntax tree,
  docstrings excluded); branch coverage on V = branch arcs executed / possible branch arcs (coverage.py's parser:
  arcs leaving a line with more than one exit); both for the green part of the suite and for all its tests that
  finish (tests that time out leave no coverage record);
- bug evidence (buggy units): the suite holds or reports a test labelled REVEALS; fix-blocking: a kept test
  labelled ENCODES.
Units come from the run's design (runs/<run>/units), so a unit whose generation produced no test counts as an
empty suite (score 0, coverage 0, no evidence; correction R1 of docs/PHASE2_REVISION_PLAN.md).
By design every test P1 keeps is kept unchanged by P2, P3 and P4, so their scores cannot be lower than P1's.
V is the version the pipeline ran on (what a tool shows its user). Writes review/out/rq3_metrics.md and
review/out/rq3_units.csv. Usage: python analysis/rq3_metrics.py
"""
import ast
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from coverage.parser import PythonParser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'analysis'))
from gbe.benchmarks import all_tasks, program  # noqa: E402
from final_numbers import design_units  # noqa: E402

RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code', 'phase2_qwen25_spec', 'phase2_qwen25_seed1',
        'phase2_qwen25_seed2', 'phase2_qwen25_seed3', 'phase2_qwen25_disguised', 'phase2_qwen35_disguised',
        'phase2_gemma4_disguised', 'phase2_qwen25_natural']
STAGES = ['GEN', 'P1', 'P2', 'P3', 'P4']


def executable_lines(source):
    tree = ast.parse(source)
    doc = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, 'value', None), ast.Constant) \
                    and isinstance(first.value.value, str):
                doc |= set(range(first.lineno, first.end_lineno + 1))
    return {n.lineno for n in ast.walk(tree) if isinstance(n, ast.stmt)} - doc


def branch_arcs(source):
    parser = PythonParser(text=source, filename='solution.py')
    parser.parse_source()
    lines = {line for line, n in parser.exit_counts().items() if n > 1}
    return {a for a in parser.arcs() if a[0] in lines}


def table(run):
    folder = ROOT / 'runs' / run
    path = folder / 'tests_rechecked.csv' if (folder / 'tests_rechecked.csv').exists() else folder / 'tests.csv'
    with open(path, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def share(part, whole):
    return round(len(part & whole) / len(whole), 4) if whole else ''


def main():
    tasks = {t['task_id']: t for t in all_tasks()[0]}
    results = {}
    for p in (ROOT / 'runs' / 'phase2_mutation' / 'results').glob('*.json'):
        d = json.loads(p.read_text(encoding='utf-8'))
        results[(d['pair_id'], d['version'])] = d
    static = {}
    out_rows = []
    for run in RUNS:
        if not (ROOT / 'runs' / run / 'tests.csv').exists():
            continue
        rows = table(run)
        units = design_units(run)
        by_stage = defaultdict(list)
        for r in rows:
            by_stage[(r['unit_id'], r['stage'])].append(r)
        files = defaultdict(set)
        for (pair, version), d in results.items():
            if version != 'fixed':  # the index is the same in both version files
                continue
            for f, entries in d['tests'].items():
                for e_run, e_unit, e_stage, _ in entries:
                    if e_run == run:
                        files[(e_unit, e_stage)].add(f)
        for unit, (pair, cond) in sorted(units.items()):
            d = results.get((pair, cond))
            if d is None:
                continue
            if (pair, cond) not in static:
                src = program(tasks[pair], cond)
                static[(pair, cond)] = (executable_lines(src), branch_arcs(src))
            exe, arcs = static[(pair, cond)]
            n_mut = len(d['mutants'])
            for stage in STAGES:
                suite = files.get((unit, stage), set())
                green = {f for f in suite if d['baseline'].get(f) == 'PASS'}
                killed = sum(1 for m in d['mutants'] if green & set(m['killed_by']))
                cov = {}
                for name, part in (('green', green), ('all', suite)):
                    lines, executed = set(), set()
                    for f in part:
                        c = d['coverage'].get(f) or {}
                        lines |= set(c.get('lines', []))
                        executed |= {tuple(a) for a in c.get('arcs', [])}
                    cov[name] = (share(lines, exe), share(executed, arcs))
                st = by_stage.get((unit, stage), [])
                kept = [r for r in st if r['final_status'] in ('KEPT', 'QUARANTINED', 'GENERATED')]
                out_rows.append({
                    'run': run, 'unit': unit, 'pair': pair, 'condition': cond, 'stage': stage,
                    'tests': len(suite), 'green': len(green), 'mutants': n_mut,
                    'mutation_score': round(killed / n_mut, 4) if n_mut else '',
                    'line_coverage': cov['green'][0], 'branch_coverage': cov['green'][1],
                    'line_coverage_all': cov['all'][0], 'branch_coverage_all': cov['all'][1],
                    'evidence': int(any(r['label'] == 'REVEALS' and r['final_status'] in ('GENERATED', 'QUARANTINED')
                                        for r in kept)) if cond == 'buggy' else '',
                    'fix_blocking': int(any(r['label'] == 'ENCODES' and r['final_status'] in ('KEPT', 'GENERATED') for r in kept))
                                    if cond == 'buggy' else ''})
    out_csv = ROOT / 'review' / 'out' / 'rq3_units.csv'
    with open(out_csv, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)

    def mean(rs, key):
        vals = [float(r[key]) for r in rs if r[key] != '']
        return statistics.mean(vals) if vals else None
    pct = lambda v: f'{100 * v:.1f}%' if v is not None else '-'
    lines = ['# RQ2 (visibility): coverage and mutation score beside bug evidence', '',
             'Computed by `analysis/rq3_metrics.py`; per-unit rows in `review/out/rq3_units.csv`. Means over all units of',
             "the run's design (a unit without tests is an empty suite), on the version the pipeline ran on; mutation score over",
             'units whose version has mutants; branch coverage over units whose version has a branch. Coverage of the green',
             'part and of all tests that finish. Evidence and fix-blocking are shares of buggy units. P2, P3 and P4 keep every',
             'P1 test unchanged, so they cannot score lower than P1.', '',
             '| Run | Condition | Suite | Units | Mean green tests | Mutation score | Line coverage (green) | Branch coverage (green) | Line coverage (all) | Branch coverage (all) | Evidence kept | Fix-blocking |',
             '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    groups = defaultdict(list)
    for r in out_rows:
        groups[(r['run'], r['condition'], r['stage'])].append(r)
    for (run, cond, stage), rs in sorted(groups.items(), key=lambda kv: (RUNS.index(kv[0][0]), kv[0][1], STAGES.index(kv[0][2]))):
        ev = mean(rs, 'evidence')
        fb = mean(rs, 'fix_blocking')
        lines.append(f"| {run} | {cond} | {stage} | {len(rs)} | {statistics.mean(r['green'] for r in rs):.1f} | "
                     f"{pct(mean(rs, 'mutation_score'))} | {pct(mean(rs, 'line_coverage'))} | {pct(mean(rs, 'branch_coverage'))} | "
                     f"{pct(mean(rs, 'line_coverage_all'))} | {pct(mean(rs, 'branch_coverage_all'))} | "
                     f"{(f'{100 * ev:.0f}%' if ev is not None else '-')} | {(f'{100 * fb:.0f}%' if fb is not None else '-')} |")
    out = ROOT / 'review' / 'out' / 'rq3_metrics.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[:14]))


if __name__ == '__main__':
    main()
