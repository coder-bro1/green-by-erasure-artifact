"""Summary tables for the Phase 2 report and the paper (item 3 after the M2 to M6 numbers).

Tables:
1. fates of bug-revealing tests per policy and false reports, per run (RQ1, RQ2), with cluster-bootstrap intervals;
2. metrics beside evidence (RQ3), buggy programs, from review/out/rq3_units.csv;
3. price of triage (RQ4): program-level D and F, break-even shares, judge with code, oracle lock;
4. S4, the judge under weaker specifications, three models (from runs/s4_judge_specs/<run>/summary.md);
5. agents: suites that lock the bug in and whether the agent's final reply names the mismatch (M5 rater), from
   runs/d11/<setting>/evaluation.json, review/m5_labels.json and review/out/m5_key.json; Wilson 95% intervals.
Writes review/out/summary_tables.md. Usage: python analysis/summary_tables.py
"""
import csv
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import final_numbers as fn  # noqa: E402

NAMES = {'phase2_qwen25_code': ('Qwen2.5-Coder 7B', 'HumanEvalFix'), 'phase2_qwen35_code': ('Qwen3.5 9B', 'HumanEvalFix'),
         'phase2_gemma4_code': ('Gemma 4 12B', 'HumanEvalFix'), 'phase2_qwen25_spec': ('Qwen2.5-Coder 7B', 'HumanEvalFix, spec in prompt'),
         'phase2_qwen25_disguised': ('Qwen2.5-Coder 7B', 'disguised'), 'phase2_qwen35_disguised': ('Qwen3.5 9B', 'disguised'),
         'phase2_gemma4_disguised': ('Gemma 4 12B', 'disguised'), 'phase2_qwen25_natural': ('Qwen2.5-Coder 7B', 'natural faults'),
         'phase2_qwen35_natural': ('Qwen3.5 9B', 'natural faults'), 'phase2_gemma4_natural': ('Gemma 4 12B', 'natural faults')}
AGENTS = [('gpt-6.1-sol_medium_frozen', 'Sol', 'HumanEvalFix'), ('gpt-6.1-sol_medium_frozen_disguised', 'Sol', 'disguised'),
          ('gpt-6.1-sol_medium_frozen_quixbugs', 'Sol', 'QuixBugs'), ('gpt-6-luna_high_frozen', 'Luna', 'HumanEvalFix'),
          ('claude-opus-5-5_medium_frozen', 'Opus', 'HumanEvalFix'), ('claude-opus-5-5_medium_frozen_disguised', 'Opus', 'disguised'),
          ('claude-opus-5-5_medium_frozen_quixbugs', 'Opus', 'QuixBugs')]
REPORT = [('gpt-6.1-sol_medium_report', 'Sol', 'HumanEvalFix'), ('gpt-6.1-sol_medium_report_quixbugs', 'Sol', 'QuixBugs'),
          ('gpt-6-luna_high_report', 'Luna', 'HumanEvalFix'), ('claude-opus-5-5_medium_report', 'Opus', 'HumanEvalFix')]


def wilson(k, n, z=1.96):
    if n == 0:
        return '-'
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return f'{k}/{n} ({100 * p:.0f}%) [{100 * max(0, centre - half):.0f}, {100 * min(1, centre + half):.0f}]'


def per_run(run):
    data = fn.rows(run)
    groups = fn.by_pair(data)
    rev = lambda p: (lambda r: r['stage'] == p and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
    fate = lambda p, f: fn.boot(groups, fn.ratio(lambda r: r['fate'] == f, rev(p)))
    fixed_judged = lambda r: r['stage'] == 'P4' and r['condition'] == 'fixed' and r['judge_verdict'] != ''
    judged_rev = lambda r: rev('P4')(r) and r['judge_verdict'] != ''
    flags = fn.program_flags(data, run)
    buggy = [f for (c, _), f in flags.items() if c == 'buggy']
    fixed = [f for (c, _), f in flags.items() if c == 'fixed']
    D_est = fn.program_rate(flags, 'buggy', lambda f: f['evidence_P4'])
    F_est = fn.program_rate(flags, 'fixed', lambda f: f['false_report'])
    return {
        'n_rev': sum(1 for r in data if rev('P2')(r)), 'pairs': len({f['pair'] for f in flags.values()}),
        'fb_added': fn.program_rate(flags, 'buggy', lambda f: f['P2'] and not f['P1']), 'D_est': D_est, 'F_est': F_est,
        'p2_inv': fate('P2', 'INVERTED'), 'p3_neu': fate('P3', 'NEUTRALIZED'), 'p3_drop': fate('P3', 'DROPPED'),
        'p4_rep': fate('P4', 'REPORTED'),
        'false': fn.boot(groups, fn.ratio(lambda r: r['final_status'] == 'QUARANTINED', fixed_judged)),
        'code_kept': fn.boot(groups, fn.ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'), judged_rev)),
        'code_false': fn.boot(groups, fn.ratio(lambda r: r['judge_with_code_verdict'] not in ('', 'TEST_WRONG'), fixed_judged)),
        'fb': {p: sum(f[p] for f in buggy) for p in ('P1', 'P2', 'P3', 'P4')}, 'n_buggy': len(buggy),
        'D': D_est[0], 'F': F_est[0],
        'n_fixed': len(fixed)}


def table_fates(stats):
    out = ['## Table 1. Fault enforcement: fate of bug-revealing tests and fix-blocking programs (RQ1)', '',
           'Shares of the bug-revealing tests generated for buggy programs; 95% cluster-bootstrap intervals over program pairs.',
           'Discard (P1), overwrite (P2) and free repair (P3) keep only tests that pass on the buggy program, so none keeps a',
           'revealing test (a property of the design). Fix-blocking: buggy programs whose final suite keeps a test that passes',
           'on the bug and fails on the fix; programs counted over the whole design, including units without tests. Every test',
           'P1 keeps is kept by P2 to P4, so the policies can only add fix-blocking programs to P1.', '',
           '| Model | Programs | Pairs | Revealing tests | Overwrite: inverted | Free repair: neutralized | Triage: reported | Triage: false reports | Fix-blocking programs, discard / overwrite / free repair / triage | Added by overwrite |',
           '|---|---|---:|---:|---|---|---|---|---|---|']
    for run, s in stats.items():
        m, prog = NAMES[run]
        fb = s['fb']
        out.append(f"| {m} | {prog} | {s['pairs']} | {s['n_rev']} | {fn.fmt(s['p2_inv'])} | {fn.fmt(s['p3_neu'])} | "
                   f"{fn.fmt(s['p4_rep'])} | {fn.fmt(s['false'])} | {fb['P1']} / {fb['P2']} / {fb['P3']} / {fb['P4']} of {s['n_buggy']} | "
                   f"{fn.fmt(s['fb_added'])} |")
    return out + ['']


def table_rq3():
    with open(ROOT / 'review' / 'out' / 'rq3_units.csv', encoding='utf-8') as fh:
        data = [r for r in csv.DictReader(fh) if r['condition'] == 'buggy']
    out = ['## Table 2. What the metrics show beside what the suite keeps (RQ2, buggy programs)', '',
           'Means over all buggy programs of the design (an empty suite scores 0) on the version the pipeline ran on; coverage of',
           'the green tests. Evidence: the suite holds or reports a test that reveals the bug. P2 to P4 keep every P1 test, so',
           'they cannot score lower than P1. Paired differences with intervals are in final_numbers.md, kill power in',
           'kill_power.md.', '',
           '| Model | Programs | Suite | Mutation score | Line coverage | Branch coverage | Bug evidence | Fix-blocking |',
           '|---|---|---|---:|---:|---:|---:|---:|']
    labels = {'GEN': 'generated, before repair', 'P1': 'discard', 'P2': 'overwrite', 'P3': 'free repair', 'P4': 'triage'}
    for run in NAMES:
        for stage in ('GEN', 'P1', 'P2', 'P3', 'P4'):
            rs = [r for r in data if r['run'] == run and r['stage'] == stage]
            if not rs:
                continue
            ms = [float(r['mutation_score']) for r in rs if r['mutation_score'] != '']
            cv = [float(r['line_coverage']) for r in rs if r['line_coverage'] != '']
            bc = [float(r['branch_coverage']) for r in rs if r['branch_coverage'] != '']
            ev = statistics.mean(int(r['evidence']) for r in rs)
            fb = statistics.mean(int(r['fix_blocking']) for r in rs)
            m, prog = NAMES[run]
            out.append(f'| {m} | {prog} | {labels[stage]} | {100 * statistics.mean(ms):.1f}% | {100 * statistics.mean(cv):.1f}% | '
                       f'{100 * statistics.mean(bc):.1f}% | {100 * ev:.0f}% | {100 * fb:.0f}% |')
    return out + ['']


def table_price(stats):
    out = ['## Table 3. The price of preservation (RQ3)', '',
           'D: buggy programs whose bug triage reports. F: correct programs with at least one false report; both over the whole',
           'design, with cluster-bootstrap intervals. Held-out pairs (outside the judge\'s 20 pilot programs) in final_numbers.md. Triage beats',
           'overwrite when the share of buggy programs exceeds p* = cF / (D + cF), c the cost of a false report relative to',
           'a missed bug. Judge with code: the same tests judged with the program source in the prompt (D10).', '',
           '| Model | Programs | D | F | p* at c = 0.25 | p* at c = 0.5 | p* at c = 1 | Judge with code: revealing tests reported | Judge with code: false reports |',
           '|---|---|---|---|---:|---:|---:|---|---|']
    for run, s in stats.items():
        m, prog = NAMES[run]
        D, F = s['D'], s['F']
        ps = ' | '.join(f'{100 * c * F / (D + c * F):.0f}%' for c in (0.25, 0.5, 1.0))
        out.append(f"| {m} | {prog} | {fn.fmt(s['D_est'])} | {fn.fmt(s['F_est'])} | {ps} | {fn.fmt(s['code_kept'])} | {fn.fmt(s['code_false'])} |")
    return out + ['']


def table_s4():
    out = ['## Table 4. The judge under weaker specifications (S4)', '',
           'Judge replayed on the same failing tests with the full docstring, without its examples, or with the signature only.',
           'Kept: a bug-revealing test of a buggy program is reported (BUG or UNSURE).', '',
           '| Model | Specification | Bug-revealing tests reported | False reports on correct programs | UNSURE verdicts |', '|---|---|---|---|---:|']
    pat = re.compile(r'^\| (full|no_examples|signature_only) \| (.+?) \| (.+?) \| (\d+) \|')
    for run in ('phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code'):
        text = (ROOT / 'runs' / 's4_judge_specs' / run / 'summary.md').read_text(encoding='utf-8')
        for line in text.splitlines():
            mt = pat.match(line)
            if mt:
                spec = {'full': 'full docstring', 'no_examples': 'no examples', 'signature_only': 'signature only'}[mt.group(1)]
                out.append(f'| {NAMES[run][0]} | {spec} | {mt.group(2)} | {mt.group(3)} | {mt.group(4)} |')
    return out + ['']


def table_agents():
    labels = json.loads((ROOT / 'review' / 'm5_labels.json').read_text(encoding='utf-8'))['answers']['b']
    key = json.loads((ROOT / 'review' / 'out' / 'm5_key.json').read_text(encoding='utf-8'))['part_b']
    named = defaultdict(lambda: [0, 0])
    for i, k in key.items():
        if k['kind'] == 'locked':
            named[k['arm']][0] += 1
            named[k['arm']][1] += labels.get(i, {}).get('answer') == 'YES'
    out = ['## Table 5. Coding agents asked to make failing tests pass with the code frozen (RQ4, arm A)', '',
           '40 buggy programs per row. Each final suite is run against the original fixed and buggy programs. Reveals',
           '(diagnostic): a test passes on the fixed and fails on the buggy program with --runxfail, so xfail-marked tests count.',
           'Active evidence: the same under plain pytest, as a CI run sees it. Encodes: a test passes on the buggy and fails on',
           'the fixed program. Encodes, reveals nothing: the suite encodes the bug and no test reveals it. Reply names the',
           'mismatch: second-rater judgement on every such suite (M5). Wilson 95% intervals.', '',
           '| Agent | Programs | Reveals (diagnostic) | Active evidence (plain pytest) | Encodes the bug | Encodes, reveals nothing | Reply names the mismatch, of those | Used skip or xfail |',
           '|---|---|---|---|---|---|---|---|']
    for setting, agent, prog in AGENTS:
        rows = [x for x in json.loads((ROOT / 'runs' / 'd11' / setting / 'evaluation.json').read_text(encoding='utf-8'))
                if x['condition'] == 'buggy']
        n = len(rows)
        locked = sum(x['suite_encodes_bug'] and not x['suite_reveals_bug'] for x in rows)
        tot, yes = named.get(setting, [0, 0])
        assert tot == locked, (setting, tot, locked)
        plain = {x['order']: x for x in json.loads((ROOT / 'runs' / 'd11' / setting / 'evaluation_plain.json').read_text(encoding='utf-8'))}
        active = sum(plain[x['order']]['active_reveals'] for x in rows)
        out.append(f"| {agent} | {prog} | {wilson(sum(x['suite_reveals_bug'] for x in rows), n)} | {wilson(active, n)} | "
                   f"{wilson(sum(x['suite_encodes_bug'] for x in rows), n)} | {wilson(locked, n)} | "
                   f"{f'{yes} of {tot}' if tot else '-'} | {wilson(sum(x['skip_or_xfail_markers'] > 0 for x in rows), n)} |")
    out += ['', '## Table 6. Agents allowed to report a suspected bug with xfail (RQ4, arm B)', '',
            'Evidence kept this way is documented, not active: under plain pytest an xfail-marked revealing test leaves the suite',
            'green on the buggy program, and with strict xfail it fails once the bug is fixed.', '',
            '| Agent | Programs | Buggy: reveals (diagnostic) | Buggy: active evidence (plain pytest) | Buggy: encodes, reveals nothing | Correct: xfail or skip used (false report) |',
            '|---|---|---|---|---|---|']
    for setting, agent, prog in REPORT:
        rows = json.loads((ROOT / 'runs' / 'd11' / setting / 'evaluation.json').read_text(encoding='utf-8'))
        b = [x for x in rows if x['condition'] == 'buggy']
        f = [x for x in rows if x['condition'] == 'fixed']
        plain = {x['order']: x for x in json.loads((ROOT / 'runs' / 'd11' / setting / 'evaluation_plain.json').read_text(encoding='utf-8'))}
        out.append(f"| {agent} | {prog} | {wilson(sum(x['suite_reveals_bug'] for x in b), len(b))} | "
                   f"{wilson(sum(plain[x['order']]['active_reveals'] for x in b), len(b))} | "
                   f"{wilson(sum(x['suite_encodes_bug'] and not x['suite_reveals_bug'] for x in b), len(b))} | "
                   f"{wilson(sum(x['skip_or_xfail_markers'] > 0 for x in f), len(f))} |")
    return out + ['', 'Agents: Sol is gpt-6.1-sol (medium reasoning) and Luna gpt-6-luna (high) in Codex CLI; Opus is',
                  'claude-opus-5-5 (medium) in Claude Code 2.1.295.', '']


def table_s5():
    """From review/out/s5_coverup.md (analysis/s5_summary.py, which also reviews the run)."""
    path = ROOT / 'review' / 'out' / 's5_coverup.md'
    if not path.exists():
        return []
    out = ['## Table 7. A real tool: CoverUp 0.6.3 with Qwen2.5-Coder 7B (S5)', '',
           'CoverUp keeps a test that passes and adds coverage, and asks the model to correct a failing test (up to three',
           'attempts). Evidence: a model answer that reveals the bug; its fate is what CoverUp kept from that code segment.', '',
           '| Programs | Buggy programs with a bug-revealing answer | Evidence dropped | Inverted | Neutralized | Reported | Buggy programs with a fix-blocking kept test | Correct programs whose kept suite catches the bug |',
           '|---|---|---:|---:|---:|---:|---|---|']
    for line in path.read_text(encoding='utf-8').splitlines():
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 12 and cells[0] in ('HumanEvalFix', 'QuixBugs', 'all'):
            nb, sig, nf, reg = int(cells[1]), int(cells[2]), int(cells[9]), int(cells[11])
            out.append(f"| {cells[0]} | {sig} of {nb} ({100 * sig / nb:.0f}%) | {cells[4]} | {cells[5]} | {cells[6]} | {cells[7]} | "
                       f"{cells[8]} of {nb} | {reg} of {nf} ({100 * reg / nf:.0f}%) |")
    return out + ['']


def main():
    stats = {run: per_run(run) for run in NAMES if (ROOT / 'runs' / run / 'tests.csv').exists()}
    lines = ['# Summary tables (Phase 2)', '', 'Computed by `analysis/summary_tables.py` after the time-out recheck.', '']
    lines += table_fates(stats) + table_rq3() + table_price(stats) + table_s4() + table_agents() + table_s5()
    out = ROOT / 'review' / 'out' / 'summary_tables.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
