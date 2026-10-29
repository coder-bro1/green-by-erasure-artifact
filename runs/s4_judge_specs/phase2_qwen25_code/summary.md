# S4: judge with weaker specifications (phase2_qwen25_code)

Computed by `scripts/s4_judge_specs.py`. Kept: a bug-revealing test on a buggy program is reported
as a likely bug (verdict BUG or UNSURE). False reports: failing tests of correct programs that the
judge does not call wrong. Tests that never reached the judge keep their P4 outcome.

| Specification | Bug-revealing tests kept | False reports on correct programs | UNSURE verdicts | Calls done |
|---|---|---|---|---|
| full | 668 of 868 (77%) | 144 of 341 (42%) | 1 | all |
| no_examples | 705 of 868 (81%) | 174 of 341 (51%) | 0 | all |
| signature_only | 531 of 868 (61%) | 153 of 341 (45%) | 0 | all |
