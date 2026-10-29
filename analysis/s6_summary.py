"""S6 summary: overwrite with the copy rules on (P2, source run) and off (P2M, model only), same generated tests.

For each S6 run (scripts/s6_model_only_overwrite.py) and its source run:
- how overwrite's inversions split between its copy rules and its model fallback (n_llm_calls of P2 rows);
- fates of the bug-revealing tests on buggy units under P2 and P2M, and the share of buggy units whose final suite
  asserts the bug (an ENCODES test), with 95% cluster-bootstrap intervals over pairs;
- once analysis/mutation_extra.py has scored the new tests: mean mutation score of discard (P1), P2 and P2M on
  buggy and correct units, the share of mutants the discard suite misses that P2M kills, the paired difference of
  the P2M rise (buggy minus correct), the discard suite plus only the P2M inverted tests, and per-test kills of
  P2M's inverted tests. Kills of P2M tests already in the Phase 2 pool come from runs/phase2_mutation/results.
Writes review/out/s6_model_only.md. Usage: python analysis/s6_summary.py [--partial]
(--partial includes unfinished runs, for checking the script only; the P2 and P2M rows then cover different units.)
"""
import argparse

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import final_numbers as fn  # noqa: E402
from kill_power import load_results  # noqa: E402

S6 = {'gemma4': 'phase2_gemma4_code', 'qwen25': 'phase2_qwen25_code'}


def share(groups, hit):
    return fn.boot(groups, lambda xs: (sum(hit(x) for x in xs), len(xs)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--partial', action='store_true')
    partial = ap.parse_args().partial
    lines = ['# S6: overwrite with and without its copy rules', '',
             'Computed by `analysis/s6_summary.py`. P2: overwrite as in the main runs (copy rules first, model when none',
             'applies). P2M: the same generated tests with the rules off, every repair by the model with overwrite\'s prompt.',
             'Shares with 95% cluster-bootstrap intervals over pairs.', '']
    fate_lines = ['## Fates of the bug-revealing tests and fault-enforcing suites (buggy units)', '',
                  '| Run | Inversions by rule (P2) | Inversions by model (P2) | Policy | Revealing tests | Inverted | Neutralized | '
                  'Dropped | Suites asserting the bug |', '|---|---:|---:|---|---:|---|---|---|---|']
    mut_lines = ['', '## Mutation score (units with mutants)', '',
                 'Remaining caught: of the mutants the discard suite misses, the share the policy\'s suite kills (pooled).',
                 'Paired: P2M rise on the buggy version minus on the fixed version of the same pair. Plus inverted: the',
                 'discard suite plus only the P2M inverted tests. Per test: mutants killed by one P2M inverted test.', '',
                 '| Run | Version | Units | Discard | P2 | P2M | P2M rise | Remaining caught (P2M) | Paired | Plus inverted | '
                 'Per inverted test | Mutant hash mismatches |', '|---|---|---:|---:|---:|---:|---|---|---|---:|---|---:|']
    results = None
    for name, source in S6.items():
        run = 's6_model_only_' + name
        manifest = ROOT / 'runs' / run / 'manifest.json'
        finished = manifest.exists() and json.loads(manifest.read_text(encoding='utf-8')).get('units') == 408
        if not (finished or (partial and manifest.exists())):
            lines.append(f'- {run}: not finished; left out.')
            continue
        src = fn.rows(source)
        p2m = [r for p in sorted((ROOT / 'runs' / run / 'units').glob('*/evaluation_P2M.json'))
               for r in json.loads(p.read_text(encoding='utf-8'))]
        inv = [r for r in src if r['stage'] == 'P2' and r['condition'] == 'buggy' and r['fate'] == 'INVERTED']
        by_model = sum(int(r['n_llm_calls'] or 0) > 0 for r in inv)
        for policy, rows in (('P2', [r for r in src if r['stage'] == 'P2']), ('P2M', p2m)):
            buggy = [r for r in rows if r['condition'] == 'buggy']
            revealing = fn.by_pair([r for r in buggy if r['gen_label'] == 'REVEALS'])
            n = sum(len(v) for v in revealing.values())
            cells = [fn.fmt(share(revealing, lambda r, f=f: r['fate'] == f)) for f in ('INVERTED', 'NEUTRALIZED', 'DROPPED')]
            # Final suite of a buggy unit asserts the bug when any kept test is labelled ENCODES.
            units = defaultdict(lambda: defaultdict(bool))
            for r in buggy:
                units[r['pair_id']][r['unit_id']] |= r['final_status'] == 'KEPT' and r['label'] == 'ENCODES'
            suites = {p: list(u.values()) for p, u in units.items()}
            fate_lines.append(f'| {run} | {len(inv) - by_model} | {by_model} | {policy} | {n} | ' + ' | '.join(cells) +
                              f' | {fn.fmt(share(suites, bool))} |')
        mutation = ROOT / 'runs' / run / 'mutation'
        extras = {}
        for p in mutation.glob('*__*.json') if mutation.exists() else []:
            d = json.loads(p.read_text(encoding='utf-8'))
            extras[(d['pair_id'], d['version'])] = d
        if not extras:
            lines.append(f'- {run}: mutation step not run yet; mutation table left out.')
            continue
        results = results or load_results()
        p2m_row = {r['test_id']: r for r in p2m}
        both = {'buggy': defaultdict(list), 'fixed': defaultdict(list)}
        per_test, mismatches = defaultdict(list), 0
        for unit, (pair, cond) in fn.design_units(source).items():
            res, extra = results.get((pair, cond)), extras.get((pair, cond))
            if res is None or extra is None or not res[0]['mutants']:
                continue
            d, kills = res
            n_mut = len(d['mutants'])
            mismatches += sum(not m['mutant_matches'] for m in extra['mutants'])
            new_kills = defaultdict(set)
            for m in extra['mutants']:
                for f in m['killed_by']:
                    new_kills[f].add(m['job_id'])
            def kills_of(f):
                return new_kills[f] if f in extra['new_tests'] else kills[f]
            def green(f):
                return (extra['baseline'] if f in extra['new_tests'] else d['baseline']).get(f) == 'PASS'
            files = defaultdict(set)
            for f, entries in d['tests'].items():
                for e_run, e_unit, e_stage, i in entries:
                    if e_run == source and e_unit == unit and e_stage in ('P1', 'P2') and green(f):
                        files[e_stage].add(f)
            inverted = set()
            for f, entries in extra['tests'].items():
                for e_run, e_unit, e_stage, i in entries:
                    if e_unit == unit and green(f):
                        files['P2M'].add(f)
                        if p2m_row[f'{unit}/t{i}']['fate'] == 'INVERTED':
                            inverted.add(f)
            union = lambda fs: set().union(*(kills_of(f) for f in fs)) if fs else set()
            k1, k2, km = union(files['P1']), union(files['P2']), union(files['P2M'])
            both[cond][pair].append((len(k1) / n_mut, len(k2) / n_mut, len(km) / n_mut, len(km - k1), n_mut - len(k1),
                                     len(union(files['P1'] | inverted)) / n_mut))
            for f in inverted:
                per_test[pair].append(len(kills_of(f)) / n_mut)
        paired = defaultdict(list)
        for pair in set(both['buggy']) & set(both['fixed']):
            for b, f in zip(both['buggy'][pair], both['fixed'][pair]):
                paired[pair].append((b[2] - b[0]) - (f[2] - f[0]))
        diff = fn.boot(paired, lambda xs: (sum(xs), len(xs)))
        for cond, label in (('buggy', 'buggy'), ('fixed', 'correct')):
            g = both[cond]
            n = sum(len(v) for v in g.values())
            if not n:
                continue
            mean = lambda i: sum(x[i] for v in g.values() for x in v) / n
            rise = fn.boot(g, lambda xs: (sum(x[2] - x[0] for x in xs), len(xs)))
            room = fn.boot(g, lambda xs: (sum(x[3] for x in xs), sum(x[4] for x in xs)))
            buggy = cond == 'buggy'
            per = fn.boot(per_test, lambda xs: (sum(xs), len(xs))) if buggy else (None, None, None)
            mut_lines.append(f'| {run} | {label} | {n} | {100 * mean(0):.1f}% | {100 * mean(1):.1f}% | {100 * mean(2):.1f}% | '
                             f'{fn.fmt(rise, 1)} | {fn.fmt(room)} | {fn.fmt(diff, 1) if buggy else ""} | '
                             f'{f"{100 * mean(5):.1f}%" if buggy else ""} | {fn.fmt(per, 1) if buggy else ""} | {mismatches} |')
    out = ROOT / 'review' / 'out' / 's6_model_only.md'
    out.write_text('\n'.join(lines + [''] + fate_lines + mut_lines) + '\n', encoding='utf-8')
    print(out.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
