# Stage C: replication on 30 BugsInPy bugs

Computed by `analysis/c1_results.py` from runs/c1_qwen35_code (complete run).
Same definitions and statistics as review/out/final_numbers.md; intervals: cluster bootstrap over bugs.

## Generated tests before repair

| Run | Tests | Reveals | Encodes | Neutral | Broken | Flaky |
|---|---:|---:|---:|---:|---:|---:|
| c1_qwen35_code, buggy | 152 | 3 (2%) | 1 (1%) | 40 (26%) | 108 (71%) | 0 (0%) |
| c1_qwen35_code, fixed | 174 | 0 (0%) | 0 (0%) | 80 (46%) | 94 (54%) | 0 (0%) |
| phase2_qwen35_code, buggy | 2038 | 759 (37%) | 84 (4%) | 771 (38%) | 424 (21%) | 0 (0%) |
| phase2_qwen35_code, fixed | 2009 | 818 (41%) | 23 (1%) | 917 (46%) | 250 (12%) | 1 (0%) |

## Fates, fix-blocking and triage

Bug-revealing tests before repair: 3.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 100% [100, 100] | 0% [0, 0] | 0% [0, 0] | 0% [0, 0] |
| P3 | 0% [0, 0] | 33% [33, 33] | 67% [67, 67] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 38% [19, 52]; 13 of 34 judged failing tests (4 BUG, 9 UNSURE) among 174 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 0% [0, 0] of those the judge saw (default judge: 0% [0, 0]); false reports 59% [32, 76]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 0% [0, 0], in erasures on buggy programs 0% [0, 0]
- Fix-blocking programs (of 30 buggy programs; 28 units of the run produced no test): discard 1, overwrite 2, free repair 1, triage 1; added by overwrite over discard 3% [0, 10] of buggy programs (discard: 3% [0, 10])
- Triage per program: bug reported for 0% [0, 0] of buggy programs (D, 0 of 30), at least one false report for 23% [10, 40] of correct programs (F, 7 of 30).
- Decision rule, triage beats overwrite above a share p* of buggy programs: -.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 33% [33, 33] with 15% [4, 27] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 88% [75, 100]

## Per bug

| Bug | Entry | Tests (buggy) | Broken | Reveals | Fix-blocking P1/P2/P3/P4 | P4 reports bug | P4 false report (fixed) |
|---|---|---:|---:|---:|---|---|---|
| cookiecutter-1 | generate_context | 10 | 1 | 0 | ./././. | no | no |
| cookiecutter-3 | read_user_choice | 0 | 0 | 0 | pending |  |  |
| httpie-3 | Session.update_headers | 0 | 0 | 0 | pending |  |  |
| httpie-4 | HTTPRequest.headers | 10 | 10 | 0 | ./././. | no | no |
| luigi-20 | Task.to_str_params | 0 | 0 | 0 | pending |  |  |
| luigi-21 | run | 13 | 1 | 3 | ./x/./. | no |  |
| luigi-25 | S3CopyToTable.run | 12 | 12 | 0 | ./././. | no |  |
| luigi-28 | HiveCommandClient.table_exists | 10 | 10 | 0 | ./././. | no | no |
| luigi-31 | CentralPlannerScheduler.get_work | 0 | 0 | 0 | pending |  |  |
| luigi-33 | Task.get_param_values | 6 | 6 | 0 | ./././. | no |  |
| luigi-4 | S3CopyToTable.copy | 0 | 0 | 0 | pending |  |  |
| pandas-119 | _add_margins | 0 | 0 | 0 | pending |  |  |
| pandas-127 | NDFrame.pct_change | 11 | 8 | 0 | ./././. | no | yes |
| pandas-161 | Categorical.fillna | 10 | 3 | 0 | ./././. | no | no |
| pandas-162 | _normalize | 10 | 10 | 0 | ./././. | no | no |
| pandas-168 | _get_grouper | 10 | 10 | 0 | ./././. | no | no |
| pandas-23 | DatetimeTimedeltaMixin.intersection | 0 | 0 | 0 | pending |  | yes |
| pandas-58 | Categorical.from_codes | 10 | 0 | 0 | ./././. | no | no |
| pandas-69 | _AtIndexer._convert_key | 0 | 0 | 0 | pending |  | yes |
| sanic-1 | Sanic.register_named_middleware | 0 | 0 | 0 | pending |  | yes |
| sanic-3 | Sanic.url_for | 10 | 10 | 0 | ./././. | no | yes |
| spacy-2 | load_model_from_path | 0 | 0 | 0 | pending |  | no |
| tornado-11 | HTTP1Connection._read_body | 11 | 11 | 0 | ./././. | no | yes |
| tornado-13 | HTTP1Connection._can_keep_alive | 10 | 10 | 0 | ./././. | no | no |
| tornado-14 | IOLoop.initialize | 0 | 0 | 0 | pending |  |  |
| tornado-2 | HTTP1Connection.write_headers | 0 | 0 | 0 | pending |  | no |
| tornado-3 | AsyncHTTPClient.close | 0 | 0 | 0 | pending |  |  |
| tornado-4 | StaticFileHandler.get | 0 | 0 | 0 | pending |  |  |
| tornado-5 | PeriodicCallback._update_next | 9 | 6 | 0 | x/x/x/x | no | yes |
| tornado-8 | WebSocketProtocol13.accept_connection | 0 | 0 | 0 | pending |  |  |

## Per project (buggy programs done)

| Project | Bugs | With a revealing test | Fix-blocking discard | Fix-blocking overwrite | Added by overwrite | P4 reports bug | P4 false report |
|---|---:|---:|---:|---:|---:|---:|---:|
| cookiecutter | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| httpie | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| luigi | 4 | 1 | 0 | 1 | 1 | 0 | 0 |
| pandas | 5 | 0 | 0 | 0 | 0 | 0 | 1 |
| sanic | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| tornado | 3 | 0 | 1 | 1 | 0 | 0 | 2 |

## Attrition

Steps 1 and 4: review/out/c1_attrition.md; steps 2 and 3: review/out/c1_install.md.
BugsInPy bugs 501; step 1 (one function in one file) 266; step 4 (prompt fits) 266; attempted in order 38; step 2 failures 8; step 3 failures 0; eligible 30.
