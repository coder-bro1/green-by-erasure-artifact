"""Independent, offline checks for the 18 October Phase 2 review.

Read saved data only. Do not call models, execute benchmark tests, or overwrite
the implementer's tables. Run from the repository with .venv's Python.
"""
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    'phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code',
    'phase2_qwen25_spec',
    *[f'phase2_qwen25_seed{i}' for i in (1, 2, 3)],
    *[f'phase2_{model}_disguised' for model in ('qwen25', 'qwen35', 'gemma4')],
    *[f'phase2_{model}_natural' for model in ('qwen25', 'qwen35', 'gemma4')],
]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as fh:
        return list(csv.DictReader(fh))


def audit_run(run):
    folder = ROOT / 'runs' / run
    pairs = json.loads((folder / 'pairs.json').read_text(encoding='utf-8'))
    table = folder / 'tests_rechecked.csv'
    rows = read_csv(table if table.exists() else folder / 'tests.csv')
    units = defaultdict(list)
    for row in rows:
        units[row['unit_id']].append(row)
    dirs = [p for p in (folder / 'units').iterdir() if p.is_dir()]
    missing = [p.name for p in dirs if p.name not in units]
    result = {'pairs': len(pairs), 'unit_directories': len(dirs),
              'units_with_rows': len(units), 'units_without_rows': missing}
    for condition in ('buggy', 'fixed'):
        selected = [rs for rs in units.values() if rs[0]['condition'] == condition]
        flags = {p: sum(any(r['stage'] == p and r['final_status'] == 'KEPT'
                           and r['label'] == 'ENCODES' for r in rs)
                        for rs in selected) for p in ('P1', 'P2', 'P3', 'P4')}
        reports = sum(any(r['stage'] == 'P4' and r['final_status'] == 'QUARANTINED'
                          and (condition == 'fixed' or r['gen_label'] == 'REVEALS')
                          for r in rs) for rs in selected)
        rev = [r for rs in selected for r in rs
               if r['stage'] == 'P2' and r['gen_label'] == 'REVEALS']
        p1_not_p2 = []
        for rs in selected:
            passed = {r['test_id'] for r in rs if r['stage'] == 'P1' and r['final_status'] == 'KEPT'}
            kept2 = {r['test_id'] for r in rs if r['stage'] == 'P2' and r['final_status'] == 'KEPT'}
            if not passed <= kept2:
                p1_not_p2.append(rs[0]['unit_id'])
        result[condition] = {
            'planned_units': len(pairs), 'units_with_rows': len(selected),
            'reported_programs': reports, 'fix_blocking': flags,
            'generated_revealing': sum(r['stage'] == 'GEN' and r['label'] == 'REVEALS'
                                      for rs in selected for r in rs),
            'overwrite_fates': dict(Counter(r['fate'] for r in rev)),
            'free_repair_revealing_kept': sum(r['stage'] == 'P3' and r['label'] == 'REVEALS'
                                             and r['final_status'] == 'KEPT'
                                             for rs in selected for r in rs),
            'p1_kept_test_ids_not_subset_of_p2': p1_not_p2,
        }
    return result


def audit_metrics():
    rows = read_csv(ROOT / 'review' / 'out' / 'rq3_units.csv')
    out = {}
    for run in RUNS[:3]:
        cells = defaultdict(dict)
        for r in rows:
            if r['run'] == run and r['condition'] == 'buggy':
                cells[r['unit']][r['stage']] = r
        stats = {}
        for key in ('mutation_score', 'line_coverage'):
            a, b, diffs = [], [], []
            for cell in cells.values():
                if cell['P1'][key] != '' and cell['P2'][key] != '':
                    x, y = float(cell['P1'][key]), float(cell['P2'][key])
                    a.append(x)
                    b.append(y)
                    diffs.append(y - x)
            stats[key] = {'eligible_units': len(diffs),
                          'p1_mean': statistics.mean(a), 'p2_mean': statistics.mean(b),
                          'mean_difference': statistics.mean(diffs),
                          'higher': sum(d > 0 for d in diffs),
                          'lower': sum(d < 0 for d in diffs)}
        out[run] = stats
    return out


def audit_agents():
    out = {}
    for path in sorted((ROOT / 'runs' / 'd11').glob('*/evaluation.json')):
        rows = json.loads(path.read_text(encoding='utf-8'))
        out[path.parent.name] = {
            c: {'n': len(rs), 'reveals_with_runxfail': sum(r['suite_reveals_bug'] for r in rs),
                'encodes_without_revealing': sum(r['suite_encodes_bug'] and not r['suite_reveals_bug'] for r in rs),
                'skip_or_xfail': sum(r['skip_or_xfail_markers'] > 0 for r in rs)}
            for c in ('buggy', 'fixed') if (rs := [r for r in rows if r['condition'] == c])
        }
    return out


def audit_raw_mutation():
    """Recompute scores from kill matrices, without the implementer's metric CSV."""
    scores = defaultdict(list)
    superset_violations = []
    coverage_status = Counter()
    total_mutants = 0
    paths = list((ROOT / 'runs' / 'phase2_mutation' / 'results').glob('*.json'))
    for path in paths:
        data = json.loads(path.read_text(encoding='utf-8'))
        coverage_status[data.get('coverage_status', 'missing')] += 1
        total_mutants += len(data['mutants'])
        if data['version'] != 'buggy':
            continue
        suites = defaultdict(set)
        for name, entries in data['tests'].items():
            if data['baseline'].get(name) != 'PASS':
                continue
            for run, unit, stage, _ in entries:
                if run in RUNS[:3] and unit.split('__')[1] == 'buggy' and stage in ('P1', 'P2'):
                    suites[run, unit, stage].add(name)
        for run in RUNS[:3]:
            units = {e[1] for entries in data['tests'].values() for e in entries
                     if e[0] == run and e[1].split('__')[1] == 'buggy'}
            for unit in units:
                p1, p2 = suites[run, unit, 'P1'], suites[run, unit, 'P2']
                if not p1 <= p2:
                    superset_violations.append([run, unit])
                if data['mutants']:
                    a, b = [sum(bool(suite.intersection(m['killed_by'])) for m in data['mutants'])
                            / len(data['mutants']) for suite in (p1, p2)]
                    scores[run].append((a, b))
    return {'version_files': len(paths), 'mutants': total_mutants,
            'coverage_status': dict(coverage_status),
            'p1_green_files_not_subset_of_p2': superset_violations,
            'main_buggy': {run: {'eligible_units': len(vals),
                                 'p1_mean': statistics.mean(v[0] for v in vals),
                                 'p2_mean': statistics.mean(v[1] for v in vals)}
                           for run, vals in scores.items()}}


def main():
    result = {'runs': {run: audit_run(run) for run in RUNS},
              'metrics': audit_metrics(), 'agents': audit_agents(),
              'raw_mutation': audit_raw_mutation()}
    c2 = read_csv(ROOT / 'review' / 'c2_labels' / 'c2_final_labels.csv')
    result['c2_final_columns'] = list(c2[0])
    result['c2_final_rows'] = len(c2)
    result['c2_final_why'] = dict(Counter(r['final_why'] for r in c2))
    result['c2_possible_erasures_disclosed'] = sum(r['final_why'] == 'E' and r['final_says'] == 'Y' for r in c2)
    prs = read_csv(ROOT / 'runs' / 'c2' / 'prs.csv')
    result['c2_prs'] = len(prs)
    result['c2_prs_with_expected_change'] = sum(int(r['expected_changes']) > 0 for r in prs)
    destination = ROOT / 'review' / 'out' / 'phase2_independent_audit.json'
    destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    for run, r in result['runs'].items():
        b, f = r['buggy'], r['fixed']
        print(f"{run}: missing={len(r['units_without_rows'])}; reveals={b['generated_revealing']}; "
              f"P2 inverted={b['overwrite_fates'].get('INVERTED', 0)}; "
              f"P3 revealing kept={b['free_repair_revealing_kept']}; "
              f"P4 programs={b['reported_programs']}/{b['planned_units']} "
              f"(table denominator {b['units_with_rows']}); "
              f"false reports={f['reported_programs']}/{f['planned_units']} "
              f"(table denominator {f['units_with_rows']})")
    print('METRICS', json.dumps(result['metrics']))
    print('RAW_MUTATION', json.dumps(result['raw_mutation']))
    print(f'Wrote {destination.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
