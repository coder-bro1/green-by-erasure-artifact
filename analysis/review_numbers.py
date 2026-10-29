"""Headline numbers per finished run for the review documents (buggy programs unless stated).

Usage: python analysis/review_numbers.py run_id [run_id ...]
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def numbers(run):
    folder = ROOT / 'runs' / run
    with open(folder / 'tests.csv', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    units = {(r['unit_id'], r['condition']) for r in rows}
    pairs = json.loads((folder / 'pairs.json').read_text(encoding='utf-8'))
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    expected_units = len(pairs) * 2 * len(manifest['config']['gen_inputs'])
    gen = [r for r in rows if r['stage'] == 'GEN']
    buggy_gen = [r for r in gen if r['condition'] == 'buggy']
    rev = [r for r in buggy_gen if r['gen_label'] == 'REVEALS']
    signal = len({r['unit_id'] for r in rev})
    buggy_units = len({r['unit_id'] for r in buggy_gen})
    out = {'run': run, 'pairs': len(pairs), 'units_with_tests': len(units), 'expected_units': expected_units,
           'gen_fail_units': expected_units - len(units), 'buggy_programs_with_tests': buggy_units,
           'signal_programs': signal, 'generated_tests_buggy': len(buggy_gen), 'revealing': len(rev)}
    for p in ('P1', 'P2', 'P3', 'P4'):
        fates = Counter(r['fate'] for r in rows if r['stage'] == p and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
        out[p] = dict(fates)
    p4_fixed = [r for r in rows if r['stage'] == 'P4' and r['condition'] == 'fixed']
    judged_fixed = [r for r in p4_fixed if r['judge_verdict']]
    out['P4_false_reports'] = f"{sum(r['final_status'] == 'QUARANTINED' for r in p4_fixed)} of {len(judged_fixed)} judged"
    modes = Counter(m for r in rows if r['stage'] in ('P2', 'P3') and r['condition'] == 'buggy'
                    and r['fate'] in ('INVERTED', 'NEUTRALIZED') for m in r['change_modes'].split('|') if m)
    out['erasure_modes'] = dict(modes.most_common(5))
    reg = lambda p: sum(r['label'] == 'REVEALS' and r['final_status'] == 'KEPT' for r in rows
                        if r['stage'] == p and r['condition'] == 'fixed')
    out['fixed_regression_revealing'] = {'P1': reg('P1'), 'P2': reg('P2')}
    return out


if __name__ == '__main__':
    for run in sys.argv[1:]:
        print(json.dumps(numbers(run)))
