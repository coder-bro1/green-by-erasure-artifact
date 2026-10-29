# S4: judge with weaker specifications (phase2_gemma4_code)

Computed by `scripts/s4_judge_specs.py`. Kept: a bug-revealing test on a buggy program is reported
as a likely bug (verdict BUG or UNSURE). False reports: failing tests of correct programs that the
judge does not call wrong. Tests that never reached the judge keep their P4 outcome.

| Specification | Bug-revealing tests kept | False reports on correct programs | UNSURE verdicts | Calls done |
|---|---|---|---|---|
| full | 863 of 908 (95%) | 60 of 144 (42%) | 40 | all |
| no_examples | 853 of 908 (94%) | 60 of 144 (42%) | 92 | all |
| signature_only | 894 of 908 (98%) | 136 of 144 (94%) | 1048 | all |
