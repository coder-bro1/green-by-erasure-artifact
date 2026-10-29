"""Cross-model Phase 1 tables for the report, computed from each run's summary.csv and
change_modes_v2_summary.json. Usage: python analysis/phase1_tables.py > review/out/phase1_tables.md"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [('Qwen2.5-Coder 7B', 'phase1_pilot'), ('Qwen3.5 9B', 'phase1_qwen35_pilot_r2'),
        ('Gemma 4 12B', 'phase1_gemma4_pilot')]


def load(run):
    rows = list(csv.DictReader(open(ROOT / 'runs' / run / 'summary.csv', encoding='utf-8')))
    return {(r['condition'], r['gen_input'], r['policy']): {k: (float(v) if k.endswith('seconds') else int(v))
            if v.replace('.', '', 1).isdigit() else v for k, v in r.items()} for r in rows}


print('### Table 1. Pre-repair signal and fates of bug-revealing tests (buggy condition)\n')
print('| Model | Input | Signal units (of 20) | Generated tests | REVEALS | P1 dropped | P2 inverted | P2 neutralized | P2 dropped | P2 ENCODES created | P3 inverted | P3 neutralized | P3 dropped | P4 reported | P4 dropped |')
print('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for name, run in RUNS:
    s = load(run)
    for arm in ('code', 'spec'):
        g, p1, p2, p3, p4 = (s[('buggy', arm, p)] for p in ('GEN', 'P1', 'P2', 'P3', 'P4'))
        print(f"| {name} | {arm} | {g['signal_units']} | {g['tests']} | {g['reveals']} | {p1['DROPPED']} | "
              f"{p2['INVERTED']} | {p2['NEUTRALIZED']} | {p2['DROPPED']} | {p2['encodes_repaired']} | "
              f"{p3['INVERTED']} | {p3['NEUTRALIZED']} | {p3['DROPPED']} | {p4['REPORTED']} | {p4['DROPPED']} |")

print('\n### Table 2. P4 triage with the v1 judge\n')
print('| Model | Input | Quarantined on buggy | of which REVEALS | False alarms on fixed |')
print('|---|---|---:|---:|---:|')
for name, run in RUNS:
    s = load(run)
    for arm in ('code', 'spec'):
        b, f = s[('buggy', arm, 'P4')], s[('fixed', arm, 'P4')]
        print(f"| {name} | {arm} | {b['quarantined']} | {b['quarantined_reveals']} | {f['quarantined']} |")

print('\n### Table 3. Fixed condition: final suite size and future-regression-revealing tests (REVEALS)\n')
print('| Model | Input | GEN size / REVEALS | P1 | P2 | P3 | P4 |')
print('|---|---|---|---|---|---|---|')
for name, run in RUNS:
    s = load(run)
    for arm in ('code', 'spec'):
        cells = [f"{s[('fixed', arm, p)]['final_size']} / {s[('fixed', arm, p)]['reveals']}" for p in ('GEN', 'P1', 'P2', 'P3', 'P4')]
        print(f"| {name} | {arm} | " + ' | '.join(cells) + ' |')

print('\n### Table 4. Change modes of erasures (classifier v2; a test can carry several modes)\n')
print('| Model | Policy | Rewritten tests | Erasures | Modes of erasures |')
print('|---|---|---:|---:|---|')
for name, run in RUNS:
    cm = json.load(open(ROOT / 'runs' / run / 'change_modes_v2_summary.json', encoding='utf-8'))
    for p in ('P2', 'P3'):
        modes = ', '.join(f'{k} {v}' for k, v in sorted(cm[p]['modes_erasures'].items(), key=lambda x: -x[1]))
        print(f"| {name} | {p} | {cm[p]['rewritten']} | {cm[p]['erasures']} | {modes} |")
