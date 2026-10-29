# S4: judge with weaker specifications (phase2_qwen35_code)

Computed by `scripts/s4_judge_specs.py`. Kept: a bug-revealing test on a buggy program is reported
as a likely bug (verdict BUG or UNSURE). False reports: failing tests of correct programs that the
judge does not call wrong. Tests that never reached the judge keep their P4 outcome.

| Specification | Bug-revealing tests kept | False reports on correct programs | UNSURE verdicts | Calls done |
|---|---|---|---|---|
| full | 711 of 759 (94%) | 115 of 270 (43%) | 65 | all |
| no_examples | 653 of 759 (86%) | 110 of 270 (41%) | 97 | all |
| signature_only | 719 of 759 (95%) | 236 of 270 (87%) | 1074 | all |
