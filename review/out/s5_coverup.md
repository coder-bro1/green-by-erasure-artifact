# S5: CoverUp 0.6.3 audit

Computed by `analysis/s5_summary.py` from `runs/s5_coverup/results.jsonl` and
CoverUp's logs. Model ollama/qwen2.5-coder:7b-instruct through the frozen Ollama, temperature 0, prompt family gpt-v1.

## Review

- Records: 408, one per pair and version: True; Counter({'buggy': 204, 'fixed': 204}); benchmarks {'HumanEvalFix': 328, 'QuixBugs': 80}.
- CoverUp exit status: {'0': 408}; total time 4.6 h, longest run 186 s.
- Model answers: 1107; records whose answers do not line up with the log: 0.
- CoverUp's verdict per answer: {'FAIL': 684, 'GAVE_UP': 265, 'COVERAGE_TIMEOUT': 7, 'ACCEPTED': 118, 'NO_CODE': 29, 'PASS_NO_COVERAGE': 4}.
- Agreement of the executor with CoverUp on the version CoverUp ran on: CoverUp: fails, ours: fails: 684; CoverUp: passes, ours: passes: 122.
- Kept tests: 118; records where accepted answers and kept files differ in number: 0; kept tests that pass on their own version: 118.
- Answers re-executed with the code CoverUp ran (truncated blocks): 161; answers without a python block (CoverUp gave up without running them, left out below): 29.
- Time-out recheck at 30 s: 19 executions, 0 label changes.
- Answers by label: {'REVEALS': 259, 'BROKEN': 794, 'NEUTRAL': 16, 'ENCODES': 9}; kept tests by version and label: {('buggy', 'NEUTRAL'): 5, ('buggy', 'ENCODES'): 9, ('fixed', 'REVEALS'): 98, ('fixed', 'NEUTRAL'): 6}.

## What CoverUp does with bug evidence

| Programs | Buggy programs | With a bug-revealing answer | Segments with evidence | Dropped | Inverted | Neutralized | Reported | Buggy programs with a fix-blocking kept test | Correct programs | With a bug-revealing answer | Kept suite reveals the bug (regression test) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HumanEvalFix | 164 | 60 | 60 | 60 | 0 | 0 | 0 | 8 | 164 | 81 | 81 |
| QuixBugs | 40 | 14 | 14 | 14 | 0 | 0 | 0 | 1 | 40 | 17 | 17 |
| all | 204 | 74 | 74 | 74 | 0 | 0 | 0 | 9 | 204 | 98 | 98 |

- The next answer after a bug-revealing answer (CoverUp has sent the failure and asked for a correction): {'REVEALS': 87, 'no further answer': 71, 'BROKEN': 3}.
- Programs with any kept test: buggy 13 of 204, correct 103 of 204.
- Other fates: {}.

