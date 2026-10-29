# Stage C: replication on 30 BugsInPy bugs

Computed by `analysis/c1_results.py` from runs/c1_qwen25_code_r2 (complete run).
Same definitions and statistics as review/out/final_numbers.md; intervals: cluster bootstrap over bugs.

## Generated tests before repair

| Run | Tests | Reveals | Encodes | Neutral | Broken | Flaky |
|---|---:|---:|---:|---:|---:|---:|
| c1_qwen25_code_r2, buggy | 281 | 2 (1%) | 2 (1%) | 49 (17%) | 228 (81%) | 0 (0%) |
| c1_qwen25_code_r2, fixed | 281 | 3 (1%) | 2 (1%) | 48 (17%) | 228 (81%) | 0 (0%) |
| phase2_qwen25_code, buggy | 2004 | 868 (43%) | 95 (5%) | 702 (35%) | 338 (17%) | 1 (0%) |
| phase2_qwen25_code, fixed | 2000 | 939 (47%) | 23 (1%) | 711 (36%) | 327 (16%) | 0 (0%) |

## Fates, fix-blocking and triage

Bug-revealing tests before repair: 2.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 50% [50, 50] | 0% [0, 0] | 50% [50, 50] | 0% [0, 0] |
| P3 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 50% [50, 50] | 50% [50, 50] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 73% [62, 84]; 99 of 136 judged failing tests (99 BUG, 0 UNSURE) among 281 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 100% [100, 100] of those the judge saw (default judge: 100% [100, 100]); false reports 83% [72, 93]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 11% [0, 32], in erasures on buggy programs 0% [0, 0]
- Fix-blocking programs (of 30 buggy programs; 4 units of the run produced no test): discard 2, overwrite 2, free repair 3, triage 2; added by overwrite over discard 0% [0, 0] of buggy programs (discard: 7% [0, 17])
- Triage per program: bug reported for 3% [0, 10] of buggy programs (D, 1 of 30), at least one false report for 73% [57, 87] of correct programs (F, 22 of 30).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 69%; c = 0.25: p* = 85%; c = 0.5: p* = 92%; c = 1.0: p* = 96%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 0% [0, 0] with 9% [5, 15] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 97% [94, 99]

## Per bug

| Bug | Entry | Tests (buggy) | Broken | Reveals | Fix-blocking P1/P2/P3/P4 | P4 reports bug | P4 false report (fixed) |
|---|---|---:|---:|---:|---|---|---|
| cookiecutter-1 | generate_context | 10 | 7 | 0 | ./././. | no | yes |
| cookiecutter-3 | read_user_choice | 10 | 8 | 0 | ./././. | no | yes |
| httpie-3 | Session.update_headers | 10 | 10 | 0 | ./././. | no | yes |
| httpie-4 | HTTPRequest.headers | 10 | 10 | 0 | ./././. | no | yes |
| luigi-20 | Task.to_str_params | 10 | 6 | 0 | ./././. | no | yes |
| luigi-21 | run | 10 | 10 | 0 | ./././. | no | yes |
| luigi-25 | S3CopyToTable.run | 10 | 3 | 0 | ./././. | no | yes |
| luigi-28 | HiveCommandClient.table_exists | 0 | 0 | 0 | pending |  |  |
| luigi-31 | CentralPlannerScheduler.get_work | 10 | 9 | 0 | ./././. | no | yes |
| luigi-33 | Task.get_param_values | 10 | 3 | 0 | ./././. | no | no |
| luigi-4 | S3CopyToTable.copy | 10 | 10 | 0 | ./././. | no | yes |
| pandas-119 | _add_margins | 10 | 10 | 0 | ./././. | no | yes |
| pandas-127 | NDFrame.pct_change | 10 | 10 | 0 | ./././. | no | yes |
| pandas-161 | Categorical.fillna | 10 | 10 | 0 | ./././. | no | yes |
| pandas-162 | _normalize | 10 | 10 | 0 | ./././. | no | yes |
| pandas-168 | _get_grouper | 10 | 9 | 0 | ./././. | no | no |
| pandas-23 | DatetimeTimedeltaMixin.intersection | 10 | 10 | 0 | ./././. | no | yes |
| pandas-58 | Categorical.from_codes | 10 | 7 | 0 | ./././. | no | yes |
| pandas-69 | _AtIndexer._convert_key | 10 | 10 | 0 | ./././. | no | yes |
| sanic-1 | Sanic.register_named_middleware | 11 | 0 | 0 | x/x/x/x | no | yes |
| sanic-3 | Sanic.url_for | 10 | 8 | 0 | ./././. | no | yes |
| spacy-2 | load_model_from_path | 10 | 10 | 0 | ./././. | no | yes |
| tornado-11 | HTTP1Connection._read_body | 10 | 10 | 0 | ./././. | no | no |
| tornado-13 | HTTP1Connection._can_keep_alive | 10 | 10 | 0 | ./././. | no | no |
| tornado-14 | IOLoop.initialize | 10 | 2 | 2 | x/x/x/x | yes | yes |
| tornado-2 | HTTP1Connection.write_headers | 10 | 10 | 0 | ./././. | no | yes |
| tornado-3 | AsyncHTTPClient.close | 10 | 6 | 0 | ./././. | no | yes |
| tornado-4 | StaticFileHandler.get | 0 | 0 | 0 | pending |  |  |
| tornado-5 | PeriodicCallback._update_next | 10 | 10 | 0 | ./././. | no | no |
| tornado-8 | WebSocketProtocol13.accept_connection | 10 | 10 | 0 | ././x/. | no | no |

## Per project (buggy programs done)

| Project | Bugs | With a revealing test | Fix-blocking discard | Fix-blocking overwrite | Added by overwrite | P4 reports bug | P4 false report |
|---|---:|---:|---:|---:|---:|---:|---:|
| cookiecutter | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| httpie | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| luigi | 6 | 0 | 0 | 0 | 0 | 0 | 5 |
| pandas | 8 | 0 | 0 | 0 | 0 | 0 | 7 |
| sanic | 2 | 0 | 1 | 1 | 0 | 0 | 2 |
| spacy | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| tornado | 7 | 1 | 1 | 1 | 0 | 1 | 3 |

## Attrition

Steps 1 and 4: review/out/c1_attrition.md; steps 2 and 3: review/out/c1_install.md.
BugsInPy bugs 501; step 1 (one function in one file) 266; step 4 (prompt fits) 266; attempted in order 38; step 2 failures 8; step 3 failures 0; eligible 30.
