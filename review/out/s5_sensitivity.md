# S5: CoverUp 0.6.3 audit (sensitivity rerun: ollama/gemma4:12b, 4096-token cap, think=False)

Computed by `analysis/s5_summary.py` from `runs/s5_sensitivity/results.jsonl` and
CoverUp's logs. Model ollama/gemma4:12b through the frozen Ollama, temperature 0, prompt family gpt-v1.

## Review

- Records: 148, one per pair and version: True; Counter({'buggy': 74, 'fixed': 74}); benchmarks {'HumanEvalFix': 120, 'QuixBugs': 28}.
- CoverUp exit status: {'0': 148}; total time 1.4 h, longest run 79 s.
- Model answers: 393; records whose answers do not line up with the log: 0.
- CoverUp's verdict per answer: {'FAIL': 76, 'ACCEPTED': 35, 'GAVE_UP': 111, 'PASS_NO_COVERAGE': 169, 'COVERAGE_TIMEOUT': 2}.
- Agreement of the executor with CoverUp on the version CoverUp ran on: CoverUp: fails, ours: fails: 76; CoverUp: passes, ours: passes: 204.
- Kept tests: 35; records where accepted answers and kept files differ in number: 0; kept tests that pass on their own version: 35.
- Answers re-executed with the code CoverUp ran (truncated blocks): 0; answers without a python block (CoverUp gave up without running them, left out below): 0.
- Time-out recheck at 30 s: 4 executions, 0 label changes.
- Answers by label: {'BROKEN': 92, 'ENCODES': 20, 'NEUTRAL': 251, 'REVEALS': 30}; kept tests by version and label: {('buggy', 'ENCODES'): 20, ('fixed', 'REVEALS'): 15}.

## What CoverUp does with bug evidence

| Programs | Buggy programs | With a bug-revealing answer | Segments with evidence | Dropped | Inverted | Neutralized | Reported | Buggy programs with a fix-blocking kept test | Correct programs | With a bug-revealing answer | Kept suite reveals the bug (regression test) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HumanEvalFix | 60 | 12 | 12 | 1 | 11 | 0 | 0 | 17 | 60 | 14 | 14 |
| QuixBugs | 14 | 1 | 1 | 0 | 1 | 0 | 0 | 3 | 14 | 1 | 1 |
| all | 74 | 13 | 13 | 1 | 12 | 0 | 0 | 20 | 74 | 15 | 15 |

- The next answer after a bug-revealing answer (CoverUp has sent the failure and asked for a correction): {'ENCODES': 9, 'REVEALS': 2, 'BROKEN': 3, 'no further answer': 1}.
- Programs with any kept test: buggy 20 of 74, correct 15 of 74.
- Other fates: {}.

