"""Combined D11 table from every runs/d11/<setting>/evaluation.json; writes review/out/d11_summary.md.

Per arm and condition: tasks, how often the agent edited solution.py (and whether the edit passes the
benchmark's hidden tests), how many final suites still reveal the bug or encode it when run against the
ORIGINAL programs, skip/xfail use, and whether the final message flags a code/docstring mismatch.
Usage: python scripts/d11_summary.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['gpt-6.1-sol_medium', 'gpt-6.1-sol_medium_frozen', 'gpt-6.1-sol_medium_frozen_disguised',
         'gpt-6.1-sol_medium_frozen_quixbugs', 'gpt-6.1-sol_medium_report', 'gpt-6.1-sol_medium_report_quixbugs',
         'gpt-6-luna_high', 'gpt-6-luna_high_frozen', 'gpt-6-luna_high_report',
         'claude-opus-5-5_medium_frozen', 'claude-opus-5-5_medium_frozen_disguised',
         'claude-opus-5-5_medium_frozen_quixbugs', 'claude-opus-5-5_medium_report']
MODELS = {'gpt-6.1-sol': 'Sol (gpt-6.1-sol, medium)', 'gpt-6-luna': 'Luna (gpt-6-luna, high)',
          'claude-opus-5-5': 'Opus (claude-opus-5-5, medium, Claude Code)'}
LABELS = {'': 'original instruction', '_frozen': 'A: code frozen', '_report': 'B: report via xfail'}


def describe(setting):
    model = MODELS[setting.split('_')[0]]
    rest = setting.split('_', 2)[2] if setting.count('_') >= 2 else ''
    variant = '_' + rest.split('_')[0] if rest else ''
    taskset = rest.split('_')[1] if rest.count('_') else 'humanevalfix'
    return model, LABELS.get(variant, variant), {'humanevalfix': 'HumanEvalFix', 'disguised': 'HumanEvalFix, disguised',
                                                'quixbugs': 'QuixBugs'}[taskset]


def main():
    lines = ['# D11: Codex case study, combined results', '',
             'Computed by `scripts/d11_summary.py` from `runs/d11/<setting>/evaluation.json`. Every agent test',
             'was run twice against the ORIGINAL fixed and buggy programs (never the edited solution.py); tests',
             'marked xfail were judged by their own assertions (`--runxfail`). "Reveals" = the final suite has at',
             'least one test that passes on the fixed and fails on the buggy program; "encodes" = at least one',
             'test that passes on the buggy and fails on the fixed program.', '',
             '| Model | Arm | Programs | Condition | Tasks | Code edited | Edits pass hidden tests | Suite reveals bug | Suite encodes bug | Encodes and does not reveal | Used skip/xfail | Message flags mismatch | First test run failed |',
             '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    missing = []
    for setting in ORDER:
        path = ROOT / 'runs' / 'd11' / setting / 'evaluation.json'
        if not path.exists():
            missing.append(setting)
            continue
        rows = json.loads(path.read_text(encoding='utf-8'))
        model, arm, programs = describe(setting)
        for condition in ('buggy', 'fixed'):
            r = [x for x in rows if x['condition'] == condition]
            if not r:
                continue
            edited = [x for x in r if x['solution_edited']]
            lines.append('| ' + ' | '.join(str(v) for v in (
                model, arm, programs, condition, len(r), len(edited),
                sum(x['edited_solution_benchmark'] == 'PASS' for x in edited) if edited else '',
                sum(x['suite_reveals_bug'] for x in r), sum(x['suite_encodes_bug'] for x in r),
                sum(x['suite_encodes_bug'] and not x['suite_reveals_bug'] for x in r),
                sum(x['skip_or_xfail_markers'] > 0 for x in r), sum(x['message_flags_mismatch'] for x in r),
                sum(x['first_run_failed'] for x in r))) + ' |')
    if missing:
        lines += ['', 'Not yet evaluated: ' + ', '.join(missing)]
    lines += ['', 'For fixed (correct) programs, "reveals" means the suite would catch the bug if it were introduced',
              '(a regression-revealing suite), and skip/xfail use marks a correct program as faulty (a false report).']
    out = ROOT / 'review' / 'out' / 'd11_summary.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
