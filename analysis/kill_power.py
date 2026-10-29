"""RQ2 (visibility): kill power of the tests that overwrite adds (stage A-3 of docs/PHASE2_REVISION_PLAN.md).

Overwrite (P2) keeps every test discard (P1) keeps and adds the tests it repaired, so its mutation score cannot be
lower (a property of the design). This script asks what the added tests contribute, from the kill matrices of
analysis/mutation_run.py (runs/phase2_mutation/results):
- groups of added tests: on buggy programs, the inverted bug-revealing tests (they now pass on the bug and assert
  it: fault-enforcing) and every other added test; on correct programs, the repairs of wrong tests (legitimate
  repairs);
- per added test: mutants it kills, and mutants it kills that the discard suite of its unit does not kill
  (marginal kills), as shares of the version's mutants; means over tests with 95% cluster-bootstrap intervals
  over pairs;
- per buggy unit: the mutation score of the discard suite plus only its inverted tests, and of the overwrite suite
  without its inverted tests, against the discard and full overwrite suites. Two estimands of the inverted tests'
  part in the rise: the share the discard suite plus inverted tests reproduces (a sufficiency share), and the share
  lost when the inverted tests are removed from the overwrite suite (a removal share). Mutant kills overlap between
  tests, so neither is an exclusive attribution and they need not add up;
- per unit on both versions: the mutation score of the discard and overwrite suites, so the rise that overwrite's
  repairs bring on correct programs (where every repair fixes a wrong test) can be set against the rise on buggy
  programs, and the paired difference of the two rises over pairs whose two versions both have mutants.
Only green tests (passing at baseline on the version) count, as for the mutation score. Units without mutants
are left out. Writes review/out/kill_power.md. Usage: python analysis/kill_power.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import final_numbers as fn  # noqa: E402

RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code', 'phase2_qwen25_spec',
        'phase2_qwen25_disguised', 'phase2_qwen35_disguised', 'phase2_gemma4_disguised']


def load_results():
    results = {}
    for p in (ROOT / 'runs' / 'phase2_mutation' / 'results').glob('*.json'):
        d = json.loads(p.read_text(encoding='utf-8'))
        kills = defaultdict(set)
        for m in d['mutants']:
            for f in m['killed_by']:
                kills[f].add(m['job_id'])
        results[(d['pair_id'], d['version'])] = (d, kills)
    return results


def main():
    results = load_results()
    lines = ['# RQ2: kill power of the tests overwrite adds', '',
             'Computed by `analysis/kill_power.py` from the kill matrices. Shares of the mutants of the version; means over',
             'added green tests with 95% cluster-bootstrap intervals over pairs. Marginal: killed by the added test and not by',
             'the discard suite of its unit.', '',
             '| Run | Added tests | Tests | Mutants killed per test | Marginal kills per test |', '|---|---|---:|---|---|']
    rise_lines = ['', '## The inverted tests and the rise (buggy programs)', '',
                  'Mean mutation score over buggy units with mutants. Reproduced: (discard + inverted - discard) / (overwrite -',
                  'discard). Lost on removal: (overwrite - overwrite without inverted) / (overwrite - discard). Kills overlap, so',
                  'the two shares are different estimands, not a decomposition.', '',
                  '| Run | Units | Discard | Discard plus inverted tests | Overwrite without inverted tests | Overwrite | Reproduced by adding inverted tests | Lost on removing them |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|']
    both_lines = ['', '## The rise from discard to overwrite on buggy and correct programs', '',
                  'Mean mutation score over units with mutants, and the rise from discard to overwrite (points of mutation',
                  'score) with 95% cluster-bootstrap intervals over pairs. Added: green tests per unit that overwrite keeps and',
                  'discard does not. Remaining caught: of the mutants the discard suite misses, the share the overwrite suite',
                  'kills (pooled over units, so the rise is set against the room left for it). Paired: rise on the buggy',
                  'version minus rise on the fixed version of the same pair, over pairs whose two versions both have mutants.', '',
                  '| Run | Version | Units | Added tests per unit | Discard | Overwrite | Rise | Remaining caught | Paired: buggy minus correct |',
                  '|---|---|---:|---:|---:|---:|---|---|---|']
    for run in RUNS:
        rows = fn.rows(run)
        row_of = {(r['unit_id'], r['stage'], r['test_id']): r for r in rows}
        units = fn.design_units(run)
        groups = {k: defaultdict(list) for k in ('inverted', 'inverted_rule', 'inverted_model', 'other_buggy',
                                                 'repair_fixed')}
        scores = []
        # pair -> [(discard score, overwrite score, added tests, mutants newly killed, mutants discard misses)]
        both = {'buggy': defaultdict(list), 'fixed': defaultdict(list)}
        for unit, (pair, cond) in units.items():
            res = results.get((pair, cond))
            udir = ROOT / 'runs' / run / 'units' / unit
            if res is None or not (udir / 'policy_P2.json').exists():
                continue
            d, kills = res
            n_mut = len(d['mutants'])
            if not n_mut:
                continue
            # Files of this unit's P1 and P2 suites, by test id.
            ids = {}
            for policy in ('P1', 'P2'):
                tests = json.loads((udir / f'policy_{policy}.json').read_text(encoding='utf-8'))['tests']
                ids[policy] = {i: t['test_id'] for i, t in enumerate(tests)}
            file_of = defaultdict(dict)
            for f, entries in d['tests'].items():
                for e_run, e_unit, e_stage, i in entries:
                    if e_run == run and e_unit == unit and e_stage in ('P1', 'P2'):
                        file_of[e_stage][ids[e_stage][i]] = f
            green = lambda f: d['baseline'].get(f) == 'PASS'
            p1_files = {f for f in file_of['P1'].values() if green(f)}
            p1_kills = set().union(*(kills[f] for f in p1_files)) if p1_files else set()
            inverted_files = set()
            for tid, f in file_of['P2'].items():
                if tid in file_of['P1'] or not green(f):
                    continue
                r = row_of.get((unit, 'P2', tid))
                if r is None:
                    continue
                if cond == 'buggy':
                    key = 'inverted' if r['fate'] == 'INVERTED' else 'other_buggy'
                    if key == 'inverted':
                        inverted_files.add(f)
                else:
                    key = 'repair_fixed'
                groups[key][pair].append((len(kills[f]) / n_mut, len(kills[f] - p1_kills) / n_mut))
                if key == 'inverted':
                    # Overwrite tries its copy rules first and calls the model only when none applies.
                    route = 'inverted_model' if int(r['n_llm_calls'] or 0) > 0 else 'inverted_rule'
                    groups[route][pair].append(groups[key][pair][-1])
            p2_files = {f for f in file_of['P2'].values() if green(f)}
            score = lambda fs: len(set().union(*(kills[f] for f in fs))) / n_mut if fs else 0.0
            p2_kills = set().union(*(kills[f] for f in p2_files)) if p2_files else set()
            both[cond][pair].append((score(p1_files), score(p2_files), len(p2_files - p1_files),
                                     len(p2_kills - p1_kills), n_mut - len(p1_kills)))
            if cond == 'buggy':
                scores.append((score(p1_files), score(p1_files | inverted_files), score(p2_files),
                               score(p2_files - inverted_files)))
        names = {'inverted': 'buggy: inverted revealing tests (fault-enforcing)', 'other_buggy': 'buggy: other added tests',
                 'repair_fixed': 'correct: repairs of wrong tests', 'inverted_rule': 'buggy: inverted by a copy rule',
                 'inverted_model': 'buggy: inverted by the model'}
        for key in ('inverted', 'inverted_rule', 'inverted_model', 'other_buggy', 'repair_fixed'):
            g = groups[key]
            n = sum(len(v) for v in g.values())
            if not n:
                continue
            kill = fn.boot(g, lambda xs: (sum(x[0] for x in xs), len(xs)))
            marg = fn.boot(g, lambda xs: (sum(x[1] for x in xs), len(xs)))
            lines.append(f'| {run} | {names[key]} | {n:,} | {fn.fmt(kill, 1)} | {fn.fmt(marg, 1)} |')
        if scores:
            m = [sum(s[i] for s in scores) / len(scores) for i in range(4)]
            share = (m[1] - m[0]) / (m[2] - m[0]) if m[2] > m[0] else float('nan')
            lost = (m[2] - m[3]) / (m[2] - m[0]) if m[2] > m[0] else float('nan')
            rise_lines.append(f'| {run} | {len(scores)} | {100 * m[0]:.1f}% | {100 * m[1]:.1f}% | {100 * m[3]:.1f}% | '
                              f'{100 * m[2]:.1f}% | {100 * share:.0f}% | {100 * lost:.0f}% |')
        paired = defaultdict(list)
        for pair in set(both['buggy']) & set(both['fixed']):
            for b, f in zip(both['buggy'][pair], both['fixed'][pair]):
                paired[pair].append((b[1] - b[0]) - (f[1] - f[0]))
        diff = fn.boot(paired, lambda xs: (sum(xs), len(xs)))
        for cond, label in (('buggy', 'buggy'), ('fixed', 'correct')):
            g = both[cond]
            n = sum(len(v) for v in g.values())
            if not n:
                continue
            mean = lambda i: sum(x[i] for v in g.values() for x in v) / n
            rise = fn.boot(g, lambda xs: (sum(x[1] - x[0] for x in xs), len(xs)))
            room = fn.boot(g, lambda xs: (sum(x[3] for x in xs), sum(x[4] for x in xs)))
            both_lines.append(f'| {run} | {label} | {n} | {mean(2):.1f} | {100 * mean(0):.1f}% | {100 * mean(1):.1f}% | '
                              f'{fn.fmt(rise, 1)} | {fn.fmt(room)} | {fn.fmt(diff, 1) if cond == "buggy" else ""} |')
    out = ROOT / 'review' / 'out' / 'kill_power.md'
    out.write_text('\n'.join(lines + rise_lines + both_lines) + '\n', encoding='utf-8')
    print('\n'.join(lines + rise_lines + both_lines))


if __name__ == '__main__':
    main()
