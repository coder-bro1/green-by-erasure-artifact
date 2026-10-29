"""Final numbers for RQ1, RQ2 and RQ4 (M2 to M4) with statistics (M6), after the time-out recheck.

Reads each run's tests_rechecked.csv (tests.csv where no recheck exists) and, for RQ3 deltas, review/out/
rq3_units.csv. Pure Python (no numerical libraries in the study environment).

Statistics:
- 95% confidence intervals by a cluster bootstrap over program pairs (2,000 resamples, fixed seed): every
  test-level and program-level rate is recomputed on resampled pairs, so the tests and both versions of one
  program stay together;
- program-level rates count every unit of the run's design (runs/<run>/units): a unit whose generation produced
  no test has no evidence, no false report and no fix-blocking test (correction R1, docs/PHASE2_REVISION_PLAN.md);
- what a policy adds over discard is reported as an increase with its interval. No significance test is run on
  its direction: every test P1 keeps is kept unchanged by P2, P3 and P4, so fix-blocking and the metrics cannot
  fall below P1 (corrections R4 and A3);
- paired differences of the RQ2 metrics (overwrite minus discard, per unit) with a bootstrap interval;
- triage also on the pairs outside the 20 pilot programs on which the judge prompt was chosen (A1);
- seed spread: the temperature-0.8 runs (seeds 1 to 3) against the temperature-0 code run on the same 40 pairs.
Decision rule (RQ4): with D the share of buggy programs whose bug triage reports, F the share of correct
programs with at least one false report, and c the cost of a false report relative to a missed bug, triage
beats overwrite when the share of buggy programs exceeds p* = c F / (D + c F). Overwrite reports nothing and
its fix-blocking suites are an extra cost not counted here, so p* is conservative.
Writes review/out/final_numbers.md. Usage: python analysis/final_numbers.py
"""
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code']
OTHER = ['phase2_qwen25_spec', 'phase2_qwen25_disguised', 'phase2_qwen35_disguised', 'phase2_gemma4_disguised',
         'phase2_qwen25_natural', 'phase2_qwen35_natural', 'phase2_gemma4_natural']
SEEDS = ['phase2_qwen25_seed1', 'phase2_qwen25_seed2', 'phase2_qwen25_seed3']
ORACLE = {'EXPECTED_CHANGED', 'EXCEPTION_EXPECTED', 'FUNCTION_SHADOWED', 'TEST_REWRITTEN', 'INPUT_CHANGED',
          'ASSERT_WEAKENED', 'ASSERT_REMOVED'}
B = 2000


def rows(run):
    folder = ROOT / 'runs' / run
    path = folder / 'tests_rechecked.csv' if (folder / 'tests_rechecked.csv').exists() else folder / 'tests.csv'
    with open(path, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def by_pair(data):
    groups = defaultdict(list)
    for r in data:
        groups[r['pair_id']].append(r)
    return groups


def boot(groups, stat, seed=20261015):
    """Point estimate and 95% interval of a ratio statistic under resampling of program pairs.

    stat(rows) returns (numerator, denominator); the estimate is the summed numerator over the summed
    denominator, so each pair is reduced to its two sums once and the resamples only add them up."""
    keys = sorted(groups)
    sums = [stat(groups[k]) for k in keys]
    num, den = sum(s[0] for s in sums), sum(s[1] for s in sums)
    if not den:
        return None, None, None
    rng = random.Random(seed)
    values = []
    for _ in range(B):
        sample = [sums[rng.randrange(len(sums))] for _ in keys]
        d = sum(s[1] for s in sample)
        if d:
            values.append(sum(s[0] for s in sample) / d)
    values.sort()
    return num / den, values[int(0.025 * len(values))], values[int(0.975 * len(values)) - 1]


def ratio(num, den):
    def f(rs):
        hits = [r for r in rs if den(r)]
        return sum(1 for r in hits if num(r)), len(hits)
    return f


def fmt(est, digits=0):
    p, lo, hi = est
    if p is None:
        return '-'
    s = f'{100 * p:.{digits}f}%'
    return s + (f' [{100 * lo:.{digits}f}, {100 * hi:.{digits}f}]' if lo is not None else '')


def mcnemar(b, c):
    """Exact two-sided McNemar p-value from discordant counts b and c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def fmt_p(p):
    return '< 0.001' if p < 0.001 else f'{p:.3f}'


def design_units(run):
    """Every unit of the run's design: unit id -> (pair id, condition), built from pairs.json and the manifest's
    configuration (pairs x versions x generation inputs) exactly as the runner names its unit folders, and checked
    against those folders where they exist (the replication package leaves them out for size)."""
    folder = ROOT / 'runs' / run
    pairs = json.loads((folder / 'pairs.json').read_text(encoding='utf-8'))
    config = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))['config']
    slug = config['model'].replace(':', '-').replace('.', '-')
    units = {}
    for p in pairs:
        for cond in ('buggy', 'fixed'):
            for gen_input in config['gen_inputs']:
                uid = f"{p['benchmark']}-{p['pair_id'].split('/', 1)[1]}__{cond}__{slug}__s{config['seed']}__{gen_input}"
                units[uid] = (p['pair_id'], cond)
    if (folder / 'units').exists():
        found = {d.name for d in (folder / 'units').iterdir() if d.is_dir()}
        if found != set(units):
            raise ValueError(f'{run}: unit folders differ from the design ({len(found)} folders, {len(units)} units)')
    return units


def pilot_pairs():
    """The 20 programs on whose Phase 1 replays the judge prompt v2b was chosen."""
    return {p['pair_id'] for p in json.loads((ROOT / 'runs' / 'phase1_pilot' / 'pairs.json').read_text(encoding='utf-8'))}


def unit_sets(data, cond):
    units = defaultdict(list)
    for r in data:
        if r['condition'] == cond:
            units[r['unit_id']].append(r)
    return units


def program_flags(data, run):
    """Per unit of the design, keyed (condition, unit): for buggy units fix-blocking under each policy, evidence
    reported by P4 and an initial signal; for correct units a false report under P4. Every flag also carries the
    unit's pair (key 'pair'), so program-level rates can be bootstrapped over pairs."""
    rows_of = defaultdict(list)
    for r in data:
        rows_of[r['unit_id']].append(r)
    flags = {}
    for unit, (pair, cond) in design_units(run).items():
        rs = rows_of.get(unit, [])
        if cond == 'buggy':
            f = {p: any(r['stage'] == p and r['final_status'] == 'KEPT' and r['label'] == 'ENCODES' for r in rs)
                 for p in ('P1', 'P2', 'P3', 'P4')}
            f['evidence_P4'] = any(r['stage'] == 'P4' and r['final_status'] == 'QUARANTINED' and r['gen_label'] == 'REVEALS' for r in rs)
            f['signal'] = any(r['stage'] == 'GEN' and r['gen_label'] == 'REVEALS' for r in rs)
        else:
            f = {'false_report': any(r['stage'] == 'P4' and r['final_status'] == 'QUARANTINED' for r in rs)}
        f['pair'] = pair
        flags[(cond, unit)] = f
    return flags


def program_rate(flags, cond, value, keep=lambda f: True):
    """Share of the condition's units with value(f) true, with a cluster-bootstrap interval over pairs."""
    groups = defaultdict(list)
    for (c, _), f in flags.items():
        if c == cond and keep(f):
            groups[f['pair']].append(f)
    return boot(groups, lambda fs: (sum(1 for f in fs if value(f)), len(fs)))


def run_section(run):
    data = rows(run)
    groups = by_pair(data)
    rev = lambda p: (lambda r: r['stage'] == p and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
    out = [f'### {run}', '']
    n_rev = sum(1 for r in data if rev('P2')(r))
    out.append(f'Bug-revealing tests before repair: {n_rev}.')
    out.append('')
    out.append('| Policy | Inverted | Neutralized | Dropped | Reported |')
    out.append('|---|---|---|---|---|')
    for p in ('P1', 'P2', 'P3', 'P4'):
        cells = [fmt(boot(groups, ratio(lambda r, fate=fate: r['fate'] == fate, rev(p))))
                 for fate in ('INVERTED', 'NEUTRALIZED', 'DROPPED', 'REPORTED')]
        out.append(f'| {p} | ' + ' | '.join(cells) + ' |')
    fixed_judged = lambda r: r['stage'] == 'P4' and r['condition'] == 'fixed' and r['judge_verdict'] != ''
    out.append('')
    # Denominator named in the paper (ICST-R5): the failing tests of correct programs that reached the judge.
    judged = [r for r in data if fixed_judged(r)]
    verdicts = Counter(r['judge_verdict'] for r in judged if r['final_status'] == 'QUARANTINED')
    n_fixed = sum(1 for r in data if r['stage'] == 'P4' and r['condition'] == 'fixed')
    out.append('- P4 false reports (failing tests of correct programs that the judge does not call wrong): '
               + fmt(boot(groups, ratio(lambda r: r['final_status'] == 'QUARANTINED', fixed_judged)))
               + f'; {sum(verdicts.values())} of {len(judged)} judged failing tests ({verdicts["BUG"]} BUG, '
               f'{verdicts["UNSURE"]} UNSURE) among {n_fixed} tests on correct programs')
    # Judge with code (D10), same tests: kept evidence and false reports had its verdict decided.
    out.append('- Judge that also sees the code (D10): bug-revealing tests kept '
               + fmt(boot(groups, ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'),
                                        lambda r: rev('P4')(r) and r['judge_verdict'] != '')))
               + ' of those the judge saw (default judge: '
               + fmt(boot(groups, ratio(lambda r: r['judge_verdict'] != 'TEST_WRONG',
                                        lambda r: rev('P4')(r) and r['judge_verdict'] != '')))
               + '); false reports '
               + fmt(boot(groups, ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'), fixed_judged))))
    # Same edit (P2): expected-value change among repairs of wrong tests (correct programs) and erasures.
    gen = {(r['unit_id'], r['test_id']): r for r in data if r['stage'] == 'GEN'}
    def same_edit(cond):
        def den(r):
            g = gen.get((r['unit_id'], r['test_id']))
            if r['stage'] != 'P2' or r['final_status'] != 'KEPT' or r['condition'] != cond or not g or g['outcome_put'] == 'PASS':
                return False
            return cond == 'fixed' or r['fate'] in ('INVERTED', 'NEUTRALIZED')
        return ratio(lambda r: 'EXPECTED_CHANGED' in r['change_modes'].split('|'), den)
    out.append('- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs '
               + fmt(boot(groups, same_edit('fixed'))) + ', in erasures on buggy programs ' + fmt(boot(groups, same_edit('buggy'))))
    # Program level, paired.
    flags = program_flags(data, run)
    buggy = [f for (c, _), f in flags.items() if c == 'buggy']
    fixed = [f for (c, _), f in flags.items() if c == 'fixed']
    n_empty = len(design_units(run)) - len({r['unit_id'] for r in data})
    out.append(f"- Fix-blocking programs (of {len(buggy)} buggy programs; {n_empty} units of the run produced no test): discard "
               f"{sum(f['P1'] for f in buggy)}, overwrite {sum(f['P2'] for f in buggy)}, free repair {sum(f['P3'] for f in buggy)}, "
               f"triage {sum(f['P4'] for f in buggy)}; added by overwrite over discard "
               + fmt(program_rate(flags, 'buggy', lambda f: f['P2'] and not f['P1']))
               + f" of buggy programs (discard: {fmt(program_rate(flags, 'buggy', lambda f: f['P1']))})")
    D_est = program_rate(flags, 'buggy', lambda f: f['evidence_P4'])
    F_est = program_rate(flags, 'fixed', lambda f: f['false_report'])
    D, F = D_est[0], F_est[0]
    out.append(f"- Triage per program: bug reported for {fmt(D_est)} of buggy programs (D, {sum(f['evidence_P4'] for f in buggy)} "
               f"of {len(buggy)}), at least one false report for {fmt(F_est)} of correct programs (F, "
               f"{sum(f['false_report'] for f in fixed)} of {len(fixed)}).")
    rule = '; '.join(f'c = {c_}: p* = {100 * c_ * F / (D + c_ * F):.0f}%' for c_ in (0.1, 0.25, 0.5, 1.0)) if D else '-'
    out.append(f'- Decision rule, triage beats overwrite above a share p* of buggy programs: {rule}.')
    # Oracle lock replayed on free repair.
    lock = {}
    for variant in ('drop', 'report'):
        def reported(r, variant=variant):
            if r['final_status'] == 'KEPT':
                return bool(set(filter(None, r['change_modes'].split('|'))) & ORACLE)
            return variant == 'report'
        failing = lambda r: gen.get((r['unit_id'], r['test_id'])) is not None and gen[(r['unit_id'], r['test_id'])]['outcome_put'] != 'PASS'
        kept_ev = boot(groups, ratio(reported, lambda r: r['stage'] == 'P3' and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS' and failing(r)))
        false_rep = boot(groups, ratio(reported, lambda r: r['stage'] == 'P3' and r['condition'] == 'fixed' and failing(r)))
        lock[variant] = (kept_ev, false_rep)
    out.append('- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle '
               'change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): '
               'unrepairable tests dropped, evidence kept ' + fmt(lock['drop'][0])
               + ' with ' + fmt(lock['drop'][1]) + ' of correct-program failures reported; unrepairable tests reported, '
               + fmt(lock['report'][0]) + ' with ' + fmt(lock['report'][1]))
    out.append('')
    return out


def heldout_section():
    """Triage on the pairs outside the judge's 20 pilot programs (A1)."""
    pilot = pilot_pairs()
    out = ['## Triage outside the 20 pilot programs (the judge prompt was chosen on their Phase 1 replays)', '',
           '| Run | Pairs | Revealing tests reported | False reports (failing tests of correct programs) | D | F |',
           '|---|---:|---|---|---|---|']
    for run in MAIN:
        data = [r for r in rows(run) if r['pair_id'] not in pilot]
        groups = by_pair(data)
        rev4 = lambda r: r['stage'] == 'P4' and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS'
        fixed_judged = lambda r: r['stage'] == 'P4' and r['condition'] == 'fixed' and r['judge_verdict'] != ''
        flags = program_flags(data, run)
        held = lambda f: f['pair'] not in pilot
        n_pairs = len({f['pair'] for f in flags.values() if held(f)})
        out.append(f"| {run} | {n_pairs} | {fmt(boot(groups, ratio(lambda r: r['fate'] == 'REPORTED', rev4)))} | "
                   f"{fmt(boot(groups, ratio(lambda r: r['final_status'] == 'QUARANTINED', fixed_judged)))} | "
                   f"{fmt(program_rate(flags, 'buggy', lambda f: f['evidence_P4'], held))} | "
                   f"{fmt(program_rate(flags, 'fixed', lambda f: f['false_report'], held))} |")
    return out + ['']


def rq3_section():
    path = ROOT / 'review' / 'out' / 'rq3_units.csv'
    if not path.exists():
        return []
    with open(path, encoding='utf-8') as fh:
        data = list(csv.DictReader(fh))
    out = ['## RQ2 (visibility): paired metric differences, overwrite minus discard, buggy programs', '',
           'Overwrite keeps every test discard keeps, unchanged, so no difference can be negative; the rows give the size.', '',
           '| Run | Units | Mutation score | Line coverage (green) | Branch coverage (green) | Line coverage (all tests) |',
           '|---|---:|---|---|---|---|']
    for run in MAIN + OTHER:
        idx = defaultdict(dict)
        for r in data:
            if r['run'] == run and r['condition'] == 'buggy':
                idx[r['unit']][r['stage']] = r
        groups = defaultdict(list)
        for unit, st in idx.items():
            if 'P1' in st and 'P2' in st:
                rec = {}
                for key, col in (('m', 'mutation_score'), ('c', 'line_coverage'), ('b', 'branch_coverage'),
                                 ('a', 'line_coverage_all')):
                    if st['P1'].get(col, '') != '' and st['P2'].get(col, '') != '':
                        rec[key] = float(st['P2'][col]) - float(st['P1'][col])
                groups[st['P1']['pair']].append(rec)
        allrec = [r for g in groups.values() for r in g]
        if not allrec:
            continue
        mean = lambda key: (lambda rs: (sum(r[key] for r in rs if key in r), sum(key in r for r in rs)))
        pts = lambda e: f'{100 * e[0]:+.1f} pts [{100 * e[1]:+.1f}, {100 * e[2]:+.1f}]' if e[0] is not None else '-'
        out.append(f"| {run} | {len(allrec)} | {pts(boot(groups, mean('m')))} | {pts(boot(groups, mean('c')))} | "
                   f"{pts(boot(groups, mean('b')))} | {pts(boot(groups, mean('a')))} |")
    return out + ['']


def seeds_section():
    out = ['## Seed spread (Qwen2.5, 40 pairs, temperature 0.8, seeds 1 to 3; temperature-0 code run on the same pairs)', '',
           '| Run | Revealing tests | Overwrite: inverted | Free repair: kept revealing | Triage: reported |', '|---|---:|---:|---:|---:|']
    subset = {r['pair_id'] for r in rows(SEEDS[0])}
    for run in ['phase2_qwen25_code'] + SEEDS:
        data = [r for r in rows(run) if r['pair_id'] in subset]
        rev = lambda p: [r for r in data if r['stage'] == p and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS']
        n = len(rev('P2'))
        inv = sum(r['fate'] == 'INVERTED' for r in rev('P2'))
        kept3 = sum(r['label'] == 'REVEALS' and r['final_status'] == 'KEPT' for r in rev('P3'))
        rep = sum(r['fate'] == 'REPORTED' for r in rev('P4'))
        out.append(f'| {run} | {n} | {inv} ({100 * inv / n:.0f}%) | {kept3} | {rep} ({100 * rep / n:.0f}%) |')
    return out + ['']


def main():
    lines = ['# Final numbers with statistics (M2 to M4, M6; revised 18 October after the external review)', '',
             'Computed by `analysis/final_numbers.py` after the time-out recheck. Brackets: 95% cluster-bootstrap',
             'intervals over program pairs (2,000 resamples). Rates of bug-revealing tests are over all bug-revealing',
             'tests of the buggy programs; P4 false reports over the failing tests of correct programs that the judge saw.', '']
    lines += ['## RQ1 and RQ3 per run', '']
    for run in MAIN + OTHER:
        if (ROOT / 'runs' / run / 'tests.csv').exists():
            lines += run_section(run)
    lines += heldout_section()
    lines += rq3_section()
    lines += seeds_section()
    out = ROOT / 'review' / 'out' / 'final_numbers.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
