"""Generate paper/numbers.tex: every number the paper states, as a LaTeX macro, read from the analysis outputs.

Sources: review/out/final_numbers.md, kill_power.md, summary_tables.md, d11_plain.md, s5_coverup.md,
s5_sensitivity.md, c2_step1.md, c2_step2.md, c2_step3.md, c2_final.md, c2_agreement.md, c1_results.md,
c1_results_qwen35_code.md, the runs' tests_rechecked.csv (raw counts), and a few counts that come from reviewed
documents (the Phase 0 census, the B-2 inspection), kept here with their source. A pattern that no longer
matches stops the script, so a changed analysis output cannot leave a stale number in the paper.
Also writes paper/numbers_sources.md (macro, value, source). Macro names use letters only; model suffixes:
QA Qwen2.5-Coder 7B, QB Qwen3.5 9B, GM Gemma 4 12B.
Usage: .venv\\Scripts\\python.exe analysis\\make_numbers.py
"""
import csv
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review' / 'out'
macros = []


def add(name, value, source):
    assert re.fullmatch(r'[A-Za-z]+', name), name
    assert all(n != name for n, _, _ in macros), f'duplicate macro {name}'
    macros.append((name, str(value), source))


def pct(s):
    return s.replace('%', r'\%')


def read(name):
    return (OUT / name).read_text(encoding='utf-8')


def want(text, pattern, source, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit(f'pattern not found in {source}: {pattern}')
    return m


def section(text, heading):
    m = want(text, rf'^### {re.escape(heading)}\n(.*?)(?=^### |^## |\Z)', heading, re.S | re.M)
    return m.group(1)


def rows(run):
    folder = ROOT / 'runs' / run
    path = folder / 'tests_rechecked.csv' if (folder / 'tests_rechecked.csv').exists() else folder / 'tests.csv'
    with open(path, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


MAIN = {'QA': 'phase2_qwen25_code', 'QB': 'phase2_qwen35_code', 'GM': 'phase2_gemma4_code'}
ROBUST = {'Spec': 'phase2_qwen25_spec', 'DisQA': 'phase2_qwen25_disguised', 'DisQB': 'phase2_qwen35_disguised',
          'DisGM': 'phase2_gemma4_disguised', 'NatQA': 'phase2_qwen25_natural', 'NatQB': 'phase2_qwen35_natural',
          'NatGM': 'phase2_gemma4_natural'}
POLICIES = (('P1', 'Discard'), ('P2', 'Overwrite'), ('P3', 'FreeRepair'), ('P4', 'Triage'))
FATES = ('Inverted', 'Neutralized', 'Dropped', 'Reported')


def cell(s):
    """'93% [88, 97]' -> ('93\\%', '[88, 97]')."""
    m = re.fullmatch(r'(-?[\d.]+)% \[(-?[\d.]+), (-?[\d.]+)\]', s.strip())
    assert m, s
    return pct(m.group(1) + '%'), f'[{m.group(2)}, {m.group(3)}]'


def final_numbers():
    fn = read('final_numbers.md')
    src = 'final_numbers.md'
    for key, run in {**MAIN, **ROBUST}.items():
        sec = section(fn, run)
        add('Revealing' + key, want(sec, r'Bug-revealing tests before repair: ([\d,]+)\.', src).group(1), f'{src} {run}')
        for policy, pname in POLICIES:
            m = want(sec, rf'^\| {policy} \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$', src, re.M)
            for fate, c in zip(FATES, m.groups()):
                p, ci = cell(c)
                add(fate + pname + key, p, f'{src} {run}')
                add(fate + pname + 'CI' + key, ci, f'{src} {run}')
        m = want(sec, r'P4 false reports .*?: (\d+% \[\d+, \d+\])', src)
        p, ci = cell(m.group(1))
        add('FalseReportsTest' + key, p, f'{src} {run}'); add('FalseReportsTestCI' + key, ci, f'{src} {run}')
        m = want(sec, r'P4 false reports .*?; (\d+) of (\d+) judged failing tests \((\d+) BUG, (\d+) UNSURE\) among (\d+) tests on correct programs', src)
        for name, v in zip(('FalseReportsCount', 'FalseReportsJudged', 'FalseReportsBug', 'FalseReportsUnsure', 'CorrectProgramTests'), m.groups()):
            add(name + key, v, f'{src} {run}')
        m = want(sec, r'kept (\d+% \[\d+, \d+\]) of those the judge saw \(default judge: (\d+% \[\d+, \d+\])\); false reports (\d+% \[\d+, \d+\])', src)
        add('JudgeCodeKept' + key, cell(m.group(1))[0], f'{src} {run}')
        add('JudgeCodeFalse' + key, cell(m.group(3))[0], f'{src} {run}')
        m = want(sec, r'correct programs (-?\d+% \[\d+, \d+\]|-), in erasures on buggy programs (-?\d+% \[\d+, \d+\]|-)', src)
        for part, name in ((m.group(1), 'SameEditCorrect'), (m.group(2), 'SameEditErasure')):
            if part != '-':
                p, ci = cell(part)
                add(name + key, p, f'{src} {run}'); add(name + 'CI' + key, ci, f'{src} {run}')
        m = want(sec, r'Fix-blocking programs \(of (\d+) buggy programs; (\d+) units? of the run produced no test\): discard (\d+), overwrite (\d+), free repair (\d+), triage (\d+); added by overwrite over discard (\d+% \[\d+, \d+\]) of buggy programs \(discard: (\d+% \[\d+, \d+\])\)', src)
        add('BuggyPrograms' + key, m.group(1), f'{src} {run}')
        add('UnitsNoTest' + key, m.group(2), f'{src} {run}')
        for pname, v in zip(('Discard', 'Overwrite', 'FreeRepair', 'Triage'), m.groups()[2:6]):
            add('FixBlocking' + pname + key, v, f'{src} {run}')
        p, ci = cell(m.group(7)); add('Added' + key, p, f'{src} {run}'); add('AddedCI' + key, ci, f'{src} {run}')
        p, ci = cell(m.group(8)); add('FixBlockingDiscardRate' + key, p, f'{src} {run}'); add('FixBlockingDiscardRateCI' + key, ci, f'{src} {run}')
        m = want(sec, r'bug reported for (\d+% \[\d+, \d+\]) of buggy programs \(D, (\d+) of (\d+)\), at least one false report for (\d+% \[\d+, \d+\]) of correct programs \(F, (\d+) of (\d+)\)', src)
        p, ci = cell(m.group(1)); add('D' + key, p, f'{src} {run}'); add('DCI' + key, ci, f'{src} {run}'); add('DCount' + key, m.group(2), f'{src} {run}')
        p, ci = cell(m.group(4)); add('F' + key, p, f'{src} {run}'); add('FCI' + key, ci, f'{src} {run}'); add('FCount' + key, m.group(5), f'{src} {run}')
        m = want(sec, r'c = 0\.1: p\* = (\d+)%; c = 0\.25: p\* = (\d+)%; c = 0\.5: p\* = (\d+)%; c = 1\.0: p\* = (\d+)%', src)
        for name, v in zip(('PstarCa', 'PstarCb', 'PstarCc', 'PstarCd'), m.groups()):
            add(name + key, pct(v + '%'), f'{src} {run} (c = 0.1, 0.25, 0.5, 1)')
    # Held-out pairs.
    for key, run in MAIN.items():
        m = want(fn, rf'^\| {run} \| 184 \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$', src, re.M)
        for name, c in zip(('HeldOutReported', 'HeldOutFalse', 'HeldOutD', 'HeldOutF'), m.groups()):
            p, ci = cell(c); add(name + key, p, f'{src} held-out'); add(name + 'CI' + key, ci, f'{src} held-out')
    # RQ2 paired differences.
    for key, run in {**MAIN, **{k: v for k, v in ROBUST.items() if k in ('Spec', 'DisQA', 'DisQB', 'DisGM', 'NatQA')}}.items():
        m = want(fn, rf'^\| {run} \| (\d+) \| \+([\d.]+) pts \[\+([\d.]+), \+([\d.]+)\] \| \+([\d.]+) pts \[\+([\d.]+), \+([\d.]+)\] \| \+([\d.]+) pts \[\+([\d.]+), \+([\d.]+)\] \| \+([\d.]+) pts \[\+([\d.]+), \+([\d.]+)\] \|$', src, re.M)
        g = m.groups()
        add('RqTwoUnits' + key, g[0], f'{src} RQ2')
        for name, i in (('MutRise', 1), ('LineRise', 4), ('BranchRise', 7), ('LineAllRise', 10)):
            add(name + key, g[i], f'{src} RQ2'); add(name + 'CI' + key, f'[{g[i + 1]}, {g[i + 2]}]', f'{src} RQ2')
    # Seeds.
    for key, run in (('SeedZero', 'phase2_qwen25_code'), ('SeedOne', 'phase2_qwen25_seed1'), ('SeedTwo', 'phase2_qwen25_seed2'), ('SeedThree', 'phase2_qwen25_seed3')):
        m = want(fn, rf'^\| {run} \| (\d+) \| (\d+) \((\d+)%\) \| (\d+) \| (\d+) \((\d+)%\) \|$', src, re.M)
        add('SeedRevealing' + key, m.group(1), f'{src} seeds'); add('SeedInverted' + key, pct(m.group(3) + '%'), f'{src} seeds')
        add('SeedReported' + key, pct(m.group(6) + '%'), f'{src} seeds')


def raw_counts():
    for key, run in MAIN.items():
        rs = rows(run)
        gen_buggy = [r for r in rs if r['stage'] == 'GEN' and r['condition'] == 'buggy']
        add('GeneratedBuggy' + key, f'{len(gen_buggy):,}', f'runs/{run} tests')
        add('UnitsWithTests' + key, len({r['unit_id'] for r in rs}), f'runs/{run} tests')
        for policy, pname in POLICIES:
            fates = Counter(r['fate'] for r in rs if r['stage'] == policy and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
            for fate in ('INVERTED', 'NEUTRALIZED', 'DROPPED', 'REPORTED'):
                add(fate.title() + pname + 'Count' + key, fates[fate], f'runs/{run} tests')


def kill_power():
    kp = read('kill_power.md'); src = 'kill_power.md'
    for key, run in {**MAIN, 'Spec': ROBUST['Spec']}.items():
        for name, label in (('Inv', r'buggy: inverted revealing tests \(fault-enforcing\)'), ('Other', 'buggy: other added tests'), ('Repair', 'correct: repairs of wrong tests')):
            m = want(kp, rf'^\| {run} \| {label} \| (\d+) \| ([\d.]+)% \[[\d., ]+\] \| ([\d.]+)% \[([\d.]+), ([\d.]+)\] \|$', src, re.M)
            add('Kill' + name + 'Tests' + key, m.group(1), src); add('Kill' + name + 'PerTest' + key, pct(m.group(2) + '%'), src)
            add('Kill' + name + 'Marginal' + key, pct(m.group(3) + '%'), src); add('Kill' + name + 'MarginalCI' + key, f'[{m.group(4)}, {m.group(5)}]', src)
        m = want(kp, rf'^\| {run} \| (\d+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \| (\d+)% \| (\d+)% \|$', src, re.M)
        add('RiseUnits' + key, m.group(1), src); add('RiseDiscardScore' + key, pct(m.group(2) + '%'), src)
        add('RiseDiscardPlusInverted' + key, pct(m.group(3) + '%'), src)
        add('RiseOverwriteWithoutInverted' + key, pct(m.group(4) + '%'), src)
        add('RiseOverwriteScore' + key, pct(m.group(5) + '%'), src)
        # Sufficiency share: adding only the inverted tests to discard reproduces this share of the overwrite gain.
        add('RiseShare' + key, pct(m.group(6) + '%'), src)
        # Removal share: removing the inverted tests from overwrite loses this share of the gain (kills overlap).
        add('RiseLostOnRemoval' + key, pct(m.group(7) + '%'), src)
    # The same discard-to-overwrite step on both versions: on correct programs every repair fixes a wrong test.
    for key, run in {**MAIN, **{k: ROBUST[k] for k in ('Spec', 'DisQA', 'DisQB', 'DisGM')}}.items():
        m = want(kp, rf'^\| {run} \| buggy \| (\d+) \| ([\d.]+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \[([\d.]+), ([\d.]+)\] \| '
                 rf'(\d+)% \[(\d+), (\d+)\] \| ([\d.]+)% \[([\d.]+), ([\d.]+)\] \|$', src, re.M)
        add('BothAddedBuggy' + key, m.group(2), src)
        add('BothRiseBuggy' + key, m.group(5), src); add('BothRiseBuggyCI' + key, f'[{m.group(6)}, {m.group(7)}]', src)
        # Of the mutants the discard suite misses, the share the overwrite suite kills (the room left for a rise).
        add('BothRoomBuggy' + key, pct(m.group(8) + '%'), src); add('BothRoomBuggyCI' + key, f'[{m.group(9)}, {m.group(10)}]', src)
        # Paired: rise on the buggy version minus rise on the fixed version of the same pair.
        add('BothRiseDiff' + key, m.group(11), src); add('BothRiseDiffCI' + key, f'[{m.group(12)}, {m.group(13)}]', src)
        m = want(kp, rf'^\| {run} \| correct \| (\d+) \| ([\d.]+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \[([\d.]+), ([\d.]+)\] \| '
                 rf'(\d+)% \[(\d+), (\d+)\] \|  \|$', src, re.M)
        add('CorrectUnits' + key, m.group(1), src); add('BothAddedCorrect' + key, m.group(2), src)
        add('CorrectMutDiscard' + key, pct(m.group(3) + '%'), src); add('CorrectMutOverwrite' + key, pct(m.group(4) + '%'), src)
        add('BothRiseCorrect' + key, m.group(5), src); add('BothRiseCorrectCI' + key, f'[{m.group(6)}, {m.group(7)}]', src)
        add('BothRoomCorrect' + key, pct(m.group(8) + '%'), src); add('BothRoomCorrectCI' + key, f'[{m.group(9)}, {m.group(10)}]', src)
    # Inversions by overwrite's copy rules and by its model fallback, per test (main runs).
    for key, run in MAIN.items():
        for name, label in (('Rule', 'buggy: inverted by a copy rule'), ('Model', 'buggy: inverted by the model')):
            m = want(kp, rf'^\| {run} \| {label} \| (\d+) \| ([\d.]+)% \[[\d., ]+\] \| ([\d.]+)% \[[\d., ]+\] \|$', src, re.M)
            add('KillInv' + name + 'Tests' + key, m.group(1), src)
            add('KillInv' + name + 'PerTest' + key, pct(m.group(2) + '%'), src)
            add('KillInv' + name + 'Marginal' + key, pct(m.group(3) + '%'), src)


def summary_tables():
    st = read('summary_tables.md'); src = 'summary_tables.md'
    names = {'QA': 'Qwen2.5-Coder 7B', 'QB': 'Qwen3.5 9B', 'GM': 'Gemma 4 12B'}
    for key, model in names.items():
        for suite, sname in (('generated, before repair', 'Gen'), ('discard', 'Discard'), ('overwrite', 'Overwrite'), ('free repair', 'FreeRepair'), ('triage', 'Triage')):
            m = want(st, rf'^\| {re.escape(model)} \| HumanEvalFix \| {re.escape(suite)} \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \| (\d+)% \| (\d+)% \|$', src, re.M)
            for name, v in zip(('Mut', 'Line', 'Branch', 'Evidence', 'FixBlockingShare'), m.groups()):
                add('Suite' + name + sname + key, pct(v + '%'), f'{src} table 2')
        for spec, sname in (('full docstring', 'Full'), ('no examples', 'NoExamples'), ('signature only', 'Signature')):
            m = want(st, rf'^\| {re.escape(model)} \| {spec} \| (\d+) of (\d+) \((\d+)%\) \| (\d+) of (\d+) \((\d+)%\) \| (\d+) \|$', src, re.M)
            add('WeakSpecReported' + sname + key, pct(m.group(3) + '%'), f'{src} table 4')
            add('WeakSpecFalse' + sname + key, pct(m.group(6) + '%'), f'{src} table 4')
            add('WeakSpecUnsure' + sname + key, m.group(7), f'{src} table 4')


def agents():
    d = read('d11_plain.md'); src = 'd11_plain.md'
    settings = {'gpt-6.1-sol_medium_frozen': 'SolFrozenHEF', 'gpt-6.1-sol_medium_frozen_disguised': 'SolFrozenDis',
                'gpt-6.1-sol_medium_frozen_quixbugs': 'SolFrozenQB', 'gpt-6-luna_high_frozen': 'LunaFrozenHEF',
                'claude-opus-5-5_medium_frozen': 'OpusFrozenHEF', 'claude-opus-5-5_medium_frozen_disguised': 'OpusFrozenDis',
                'claude-opus-5-5_medium_frozen_quixbugs': 'OpusFrozenQB', 'gpt-6.1-sol_medium_report': 'SolReportHEF',
                'gpt-6.1-sol_medium_report_quixbugs': 'SolReportQB', 'gpt-6-luna_high_report': 'LunaReportHEF',
                'claude-opus-5-5_medium_report': 'OpusReportHEF'}
    for setting, key in settings.items():
        for cond in ('buggy', 'fixed'):
            m = re.search(rf'^\| {re.escape(setting)} \| {cond} \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$', d, re.M)
            if not m:
                continue
            for name, v in zip(('Tasks', 'Reveals', 'Active', 'Encodes', 'EncodesNothing', 'RedBuggy', 'CISep'), m.groups()):
                add(key + cond.title() + name, v, src)
    # d11_summary.md: code edits under the original instruction, and skip or xfail use (on a correct program a
    # false report).
    s = read('d11_summary.md')
    arms = {'original instruction': 'Open', 'A: code frozen': 'Frozen', 'B: report via xfail': 'Report'}
    progs = {'HumanEvalFix': 'HEF', 'HumanEvalFix, disguised': 'Dis', 'QuixBugs': 'QB'}
    rows = re.findall(r'^\| (Sol|Luna|Opus) \([^)]*\) \| ([^|]+?) \| ([^|]+?) \| (buggy|fixed) \| \d+ \| (\d+) \| (\d*) \| '
                      r'\d+ \| \d+ \| \d+ \| (\d+) \|', s, re.M)
    if not rows:
        raise SystemExit('pattern not found in d11_summary.md')
    for model, arm, prog, cond, edited, passing, skip in rows:
        key = model + arms[arm] + progs[prog] + cond.title()
        add(key + 'CodeEdited', edited, 'd11_summary.md'); add(key + 'SkipXfail', skip, 'd11_summary.md')
        if passing:
            add(key + 'EditsPassHidden', passing, 'd11_summary.md')
    add('AgentRepliesNameMismatch', 46, 'PHASE2_REPORT section 5.5 (rater labels)')
    add('AgentBugEncodingSuites', 51, 'PHASE2_REPORT section 5.5 (18 + 13 + 8 Sol, 12 Luna)')


def coverup():
    for key, name in (('CoverUpQA', 's5_coverup.md'), ('CoverUpGM', 's5_sensitivity.md')):
        t = read(name)
        m = want(t, r'^\| all \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$', name, re.M)
        for f, v in zip(('BuggyPrograms', 'WithRevealing', 'Segments', 'Dropped', 'Inverted', 'Neutralized', 'Reported', 'FixBlocking', 'CorrectPrograms', 'CorrectWithRevealing', 'KeptRegression'), m.groups()):
            add(key + f, v, name)
        m = want(t, r'Model answers: ([\d,]+);', name); add(key + 'Answers', m.group(1), name)
        m = want(t, r"Answers by label: \{[^}]*'BROKEN': (\d+)", name); add(key + 'BrokenAnswers', m.group(1), name)
    t = read('s5_sensitivity.md')
    m = want(t, r"next answer after a bug-revealing answer .*?: \{'ENCODES': (\d+), 'REVEALS': (\d+), 'BROKEN': (\d+)", 's5_sensitivity.md')
    add('CoverUpGMNextEncodes', m.group(1), 's5_sensitivity.md'); add('CoverUpGMNextReveals', m.group(2), 's5_sensitivity.md')


def pull_requests():
    s1 = read('c2_step1.md')
    m = want(s1, r'^\| all \| ([\d,]+) \| ([\d,]+) \| (\d+) \((\d+)%\) \| (\d+) \| (\d+) \| ([\d,]+) \| (\d+) \|$', 'c2_step1.md', re.M)
    for name, v in zip(('PRPython', 'PRTouchTestsAndCode', 'PRCandidates', 'PRCandidateShare', 'PRMerged', 'PRTestEditLater', 'PRExpectedChanges', 'PRSkipAdded'), m.groups()):
        add(name, pct(v + '%') if name == 'PRCandidateShare' else v, 'c2_step1.md')
    s2 = read('c2_step2.md')
    m = want(s2, r'^\| all \| with \| (\d+) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \|$', 'c2_step2.md', re.M)
    g = m.groups()
    for name, i in (('PRMentionsTests', 1), ('PRExplainsRegex', 3), ('PRHumanComment', 5), ('PRCommentOnTestFile', 7), ('PRContextShowsAssert', 9), ('PRAnchoredOnAssert', 11), ('PRChangesRequested', 13), ('PRMergedWith', 15)):
        add(name, g[i], 'c2_step2.md'); add(name + 'Share', pct(g[i + 1] + '%'), 'c2_step2.md')
    s3 = read('c2_step3.md')
    m = want(s3, r'^\| all \| (\d+) \((\d+)\) \| (\d+) \((\d+)\) \| (\d+) \((\d+)\) \| (\d+) \((\d+)\) \|', 'c2_step3.md', re.M)
    for name, v in zip(('PRAssertsMerged', 'PRAssertsMergedPRs', 'PRRestored', 'PRRestoredPRs', 'PRChangedAgain', 'PRChangedAgainPRs', 'PRUntouched', 'PRUntouchedPRs'), m.groups()):
        add(name, v, 'c2_step3.md')
    f = read('c2_final.md')
    m = want(f, r'Real expectation changes \(not M\): (\d+) of (\d+) in the sample \((\d+)% \[(\d+), (\d+)\]\); weighted to all candidates \d+%, about (\d+) pull requests', 'c2_final.md')
    add('PRRealSample', m.group(1), 'c2_final.md'); add('PRSampleCases', m.group(2), 'c2_final.md')
    add('PRRealShare', pct(m.group(3) + '%'), 'c2_final.md'); add('PRRealShareCI', f'[{m.group(4)}, {m.group(5)}]', 'c2_final.md'); add('PRRealCount', m.group(6), 'c2_final.md')
    m = want(f, r'The description says that an existing expectation changed: (\d+) of (\d+) \((\d+)% \[(\d+), (\d+)\]\)', 'c2_final.md')
    add('PRSaysCount', m.group(1), 'c2_final.md'); add('PRSays', pct(m.group(3) + '%'), 'c2_final.md'); add('PRSaysCI', f'[{m.group(4)}, {m.group(5)}]', 'c2_final.md')
    for label, name in (('I: intended behaviour change', 'I'), ('W: wrong test repaired', 'W'), ('E: possible erasure', 'E'), ('M: no real change \\(matcher error\\)', 'M'), ("U: can't tell", 'U')):
        m = want(f, rf'^\| {label} \| (\d+) \| (\d+)% \[(\d+), (\d+)\] \|', 'c2_final.md', re.M)
        add('PRLabel' + name, m.group(1), 'c2_final.md'); add('PRLabel' + name + 'Share', pct(m.group(2) + '%'), 'c2_final.md')
    a = read('c2_agreement.md')
    add('PRKappa', want(a, r'WHY, five labels: observed agreement \d+%, Cohen kappa ([\d.]+)\.', 'c2_agreement.md').group(1), 'c2_agreement.md')
    add('PRKappaNoU', want(a, r'neither rater marked U: agreement \d+%, kappa ([\d.]+)\.', 'c2_agreement.md').group(1), 'c2_agreement.md')
    # Stage B-2 reading of the 13 cases first labelled E (docs/reviews/C2_REPLAY_B2.md, section 3).
    for name, v in (('PREFirst', 13), ('PREForeign', 5), ('PREMatcher', 2), ('PREInfra', 1), ('PREIntended', 4), ('PREExecuted', 1), ('PREConfirmed', 0)):
        add(name, v, 'docs/reviews/C2_REPLAY_B2.md section 3')


def real_bugs():
    for key, name, run in (('RealQA', 'c1_results.md', 'c1_qwen25_code_r2'), ('RealQB', 'c1_results_qwen35_code.md', 'c1_qwen35_code')):
        t = read(name)
        for cond in ('buggy', 'fixed'):
            m = want(t, rf'^\| {run}, {cond} \| (\d+) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \| (\d+) \((\d+)%\) \|$', name, re.M)
            g = m.groups()
            add(key + cond.title() + 'Tests', g[0], name)
            for f, i in (('Reveals', 1), ('Encodes', 3), ('Neutral', 5), ('Broken', 7), ('Flaky', 9)):
                add(key + cond.title() + f, g[i], name); add(key + cond.title() + f + 'Share', pct(g[i + 1] + '%'), name)
        m = want(t, r'Fix-blocking programs \(of (\d+) buggy programs; (\d+) units? of the run produced no test\): discard (\d+), overwrite (\d+), free repair (\d+), triage (\d+); added by overwrite over discard (\d+)% \[', name)
        add(key + 'UnitsNoTest', m.group(2), name)
        for pname, v in zip(('Discard', 'Overwrite', 'FreeRepair', 'Triage'), m.groups()[2:6]):
            add(key + 'FixBlocking' + pname, v, name)
        add(key + 'Added', pct(m.group(7) + '%'), name)
        m = want(t, r'bug reported for \d+% \[\d+, \d+\] of buggy programs \(D, (\d+) of (\d+)\), at least one false report for (\d+)% \[(\d+), (\d+)\] of correct programs \(F, (\d+) of (\d+)\)', name)
        add(key + 'DCount', m.group(1), name); add(key + 'F', pct(m.group(3) + '%'), name); add(key + 'FCI', f'[{m.group(4)}, {m.group(5)}]', name); add(key + 'FCount', m.group(6), name)
        rs = rows(run)
        add(key + 'UnitsWithTests', len({r['unit_id'] for r in rs}), f'runs/{run} tests')
        for policy, pname in POLICIES:
            fates = Counter(r['fate'] for r in rs if r['stage'] == policy and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
            add(key + 'Inverted' + pname, fates['INVERTED'], f'runs/{run} tests')
            add(key + 'Reported' + pname, fates['REPORTED'], f'runs/{run} tests')
    m = want(read('c1_results.md'), r'BugsInPy bugs (\d+); step 1 .*? (\d+); step 4 .*? (\d+); attempted in order (\d+); step 2 failures (\d+); step 3 failures (\d+); eligible (\d+)\.', 'c1_results.md')
    for name, v in zip(('RealBugsAll', 'RealStepOne', 'RealStepFour', 'RealAttempted', 'RealInstallFail', 'RealTestFail', 'RealEligible'), m.groups()):
        add(name, v, 'c1_results.md attrition')
    add('RealProjects', 7, 'c1_install.md (projects with an eligible bug)')
    # Section 10 of the C1 protocol: the developers' own revealing tests through the policies.
    run = 'c1_devtests_qwen25_r2'
    rs = rows(run)
    gen = [r for r in rs if r['stage'] == 'GEN' and r['condition'] == 'buggy']
    add('DevTests', len(gen), f'runs/{run} tests'); add('DevBugs', len({r['pair_id'] for r in gen}), f'runs/{run} tests')
    add('DevRevealing', sum(r['label'] == 'REVEALS' for r in gen), f'runs/{run} tests')
    for policy, pname in POLICIES:
        fates = Counter(r['fate'] for r in rs if r['stage'] == policy and r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS')
        for fate in ('INVERTED', 'NEUTRALIZED', 'DROPPED', 'REPORTED'):
            add('Dev' + fate.title() + pname, fates[fate], f'runs/{run} tests')
        fb = {r['pair_id'] for r in rs if r['stage'] == policy and r['condition'] == 'buggy' and r['final_status'] == 'KEPT' and r['label'] == 'ENCODES'}
        add('DevFixBlocking' + pname, len(fb), f'runs/{run} tests')
    shadow = sum('FUNCTION_SHADOWED' in r['change_modes'] for r in rs if r['stage'] == 'P3' and r['condition'] == 'buggy')
    add('DevShadowedFreeRepair', shadow, f'runs/{run} tests (P3 rewrites that define the function under test locally)')
    judged_wrong = sum(r['judge_verdict'] == 'TEST_WRONG' for r in rs if r['stage'] == 'P4' and r['condition'] == 'buggy')
    add('DevJudgedWrong', judged_wrong, f'runs/{run} tests')
    add('DevJudgeUnseen', sum(r['stage'] == 'P4' and r['condition'] == 'buggy' and r['fate'] == 'DROPPED' and not r['judge_verdict'] for r in rs), f'runs/{run} tests')


def constants():
    add('CensusTotal', 22, 'docs/PHASE0_NOVELTY.md section 5'); add('CensusOverwrite', 12, 'docs/PHASE0_NOVELTY.md section 5')
    add('CensusDiscard', 4, 'docs/PHASE0_NOVELTY.md section 5'); add('CensusKeep', 3, 'docs/PHASE0_NOVELTY.md section 5')
    add('CensusOther', 3, 'docs/PHASE0_NOVELTY.md section 5 (2 score failures as wrong tests, 1 strips LLM assertions)')
    add('Pairs', 204, 'runs/*/pairs.json'); add('PairsHEF', 164, 'runs/*/pairs.json'); add('PairsQB', 40, 'runs/*/pairs.json')
    add('PairsDisguised', 40, 'configs/disguised.json'); add('PairsNatural', 25, 'configs/natural.json')
    add('HeldOutPairs', 184, 'final_numbers.md'); add('PilotPairs', 20, 'runs/phase1_pilot/pairs.json')
    add('SeedPairs', len(json.loads((ROOT / 'runs' / 'phase2_qwen25_seed1' / 'pairs.json').read_text(encoding='utf-8'))),
        'runs/phase2_qwen25_seed1/pairs.json')


def classifier_validation():
    """M5: the change-mode classifier against the human rater (review/out/m5_agreement.md, part A)."""
    text = read('m5_agreement.md')
    add('MFiveSample', want(text, r'## Part A: change modes \((\d+) repaired tests\)', 'm5_agreement.md').group(1), 'm5_agreement.md')
    m = want(text, r'^\| EXPECTED_CHANGED \| (\d+) \| (\d+) \| (\d+) \|', 'm5_agreement.md', re.M)
    add('MFiveExpectedRater', m.group(1), 'm5_agreement.md'); add('MFiveExpectedBoth', m.group(3), 'm5_agreement.md')
    add('MFiveExpectedClassifier', m.group(2), 'm5_agreement.md')


def mutation_totals():
    """Size of the mutation analysis, from the kill matrices (one file per program version)."""
    src = 'runs/phase2_mutation/results/*.json'
    files = sorted((ROOT / 'runs' / 'phase2_mutation' / 'results').glob('*.json'))
    data = [json.loads(f.read_text(encoding='utf-8')) for f in files]
    add('MutVersions', len(data), src); add('Mutants', f"{sum(len(d['mutants']) for d in data):,}", src)
    main = [d for d in data if d['benchmark'] in ('HumanEvalFix', 'QuixBugs')]  # the 204 pairs of the main arm
    add('MutVersionsMain', len(main), src)
    add('MutantsMain', f"{sum(len(d['mutants']) for d in main):,}", src)
    add('MutNoMutantMain', sum(1 for d in main if not d['mutants']), src)
    add('MutNoMutantBuggyMain', sum(1 for d in main if not d['mutants'] and d['version'] == 'buggy'), src)


def model_only():
    """S6: overwrite with its copy rules off (review/out/s6_model_only.md); Mo = model only, GM/QA = model."""
    src = 's6_model_only.md'
    text = read(src)
    ci = r'(\d+)% \[(\d+), (\d+)\]'
    for key, name in (('GM', 'gemma4'), ('QA', 'qwen25')):
        run = 's6_model_only_' + name
        m = want(text, rf'^\| {run} \| (\d+) \| (\d+) \| P2M \| (\d+) \| {ci} \| {ci} \| {ci} \| {ci} \|$', src, re.M)
        add('MoRuleInv' + key, m.group(1), src); add('MoModelInv' + key, m.group(2), src)
        add('MoRevealing' + key, m.group(3), src)
        for i, label in enumerate(('Inverted', 'Neutralized', 'Dropped', 'Suites')):
            g = 4 + 3 * i
            add('Mo' + label + key, pct(m.group(g) + '%'), src)
            add('Mo' + label + 'CI' + key, f'[{m.group(g + 1)}, {m.group(g + 2)}]', src)
        f1 = r'(-?[\d.]+)% \[(-?[\d.]+), (-?[\d.]+)\]'
        m = want(text, rf'^\| {run} \| buggy \| (\d+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \| {f1} \| {ci} \| {f1} \| '
                       rf'([\d.]+)% \| {f1} \| (\d+) \|$', src, re.M)
        add('MoMutDiscardBuggy' + key, pct(m.group(2) + '%'), src); add('MoMutRulesBuggy' + key, pct(m.group(3) + '%'), src)
        add('MoMutModelBuggy' + key, pct(m.group(4) + '%'), src)
        add('MoRiseBuggy' + key, m.group(5), src); add('MoRiseBuggyCI' + key, f'[{m.group(6)}, {m.group(7)}]', src)
        add('MoRoomBuggy' + key, pct(m.group(8) + '%'), src); add('MoRoomBuggyCI' + key, f'[{m.group(9)}, {m.group(10)}]', src)
        add('MoRiseDiff' + key, m.group(11), src); add('MoRiseDiffCI' + key, f'[{m.group(12)}, {m.group(13)}]', src)
        add('MoPlusInverted' + key, pct(m.group(14) + '%'), src)
        add('MoKillPerInv' + key, pct(m.group(15) + '%'), src); add('MoKillPerInvCI' + key, f'[{m.group(16)}, {m.group(17)}]', src)
        add('MoMutantMismatch' + key, m.group(18), src)
        m = want(text, rf'^\| {run} \| correct \| (\d+) \| ([\d.]+)% \| ([\d.]+)% \| ([\d.]+)% \| {f1} \| {ci} \|  \|  \|  \| '
                       rf'(\d+) \|$', src, re.M)
        add('MoMutDiscardCorrect' + key, pct(m.group(2) + '%'), src); add('MoMutModelCorrect' + key, pct(m.group(4) + '%'), src)
        add('MoRiseCorrect' + key, m.group(5), src); add('MoRiseCorrectCI' + key, f'[{m.group(6)}, {m.group(7)}]', src)
        add('MoRoomCorrect' + key, pct(m.group(8) + '%'), src)
        add('MoRoomCorrectCI' + key, f'[{m.group(9)}, {m.group(10)}]', src)


def main():
    final_numbers(); raw_counts(); kill_power(); summary_tables(); agents(); coverup(); pull_requests(); real_bugs(); constants()
    mutation_totals(); classifier_validation()
    if (OUT / 's6_model_only.md').exists():
        model_only()
    commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (ROOT / 'paper').mkdir(exist_ok=True)
    lines = [f'% Generated by analysis/make_numbers.py on {time.strftime("%Y-%m-%d %H:%M")} at commit {commit}. Do not edit.']
    lines += [f'\\newcommand{{\\{n}}}{{{v}}}' for n, v, _ in sorted(macros)]
    (ROOT / 'paper' / 'numbers.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    doc = ['# Sources of the numbers in the paper', '', f'Generated with paper/numbers.tex at commit {commit}.', '',
           '| Macro | Value | Source |', '|---|---|---|'] + [f'| \\{n} | {v} | {s} |' for n, v, s in sorted(macros)]
    (ROOT / 'paper' / 'numbers_sources.md').write_text('\n'.join(doc) + '\n', encoding='utf-8')
    print(f'{len(macros)} macros written')


if __name__ == '__main__':
    main()
