# D11: final suites under plain pytest against the diagnostic evaluation

Computed by `analysis/d11_plain.py`. Reveals (diagnostic) and encodes come from `evaluation.json` (`--runxfail`);
active evidence and the CI columns from running the same final suites with plain pytest. CI separates the
versions: the suite is red on the buggy program and green on the fixed one.

| Setting | Condition | Tasks | Reveals (diagnostic) | Active evidence (plain pytest) | Encodes the bug | Encodes, reveals nothing | Red on buggy | CI separates the versions |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol_medium_frozen | buggy | 40 | 21 | 2 | 20 | 18 | 2 | 1 |
| gpt-6.1-sol_medium_frozen_disguised | buggy | 40 | 27 | 2 | 15 | 13 | 2 | 2 |
| gpt-6.1-sol_medium_frozen_quixbugs | buggy | 40 | 31 | 0 | 11 | 8 | 0 | 0 |
| gpt-6-luna_high_frozen | buggy | 40 | 17 | 0 | 12 | 12 | 0 | 0 |
| claude-opus-5-5_medium_frozen | buggy | 40 | 40 | 10 | 12 | 0 | 10 | 9 |
| claude-opus-5-5_medium_frozen_disguised | buggy | 40 | 40 | 20 | 1 | 0 | 20 | 20 |
| claude-opus-5-5_medium_frozen_quixbugs | buggy | 40 | 40 | 1 | 9 | 0 | 1 | 1 |
| gpt-6.1-sol_medium_report | buggy | 40 | 40 | 0 | 2 | 0 | 0 | 0 |
| gpt-6.1-sol_medium_report | fixed | 40 | 39 | 38 | 2 | 0 | 40 | 40 |
| gpt-6.1-sol_medium_report_quixbugs | buggy | 40 | 40 | 0 | 2 | 0 | 0 | 0 |
| gpt-6.1-sol_medium_report_quixbugs | fixed | 40 | 38 | 37 | 0 | 0 | 40 | 40 |
| gpt-6-luna_high_report | buggy | 40 | 33 | 0 | 2 | 0 | 0 | 0 |
| gpt-6-luna_high_report | fixed | 40 | 34 | 34 | 1 | 0 | 35 | 35 |
| claude-opus-5-5_medium_report | buggy | 40 | 40 | 0 | 1 | 0 | 0 | 0 |
| claude-opus-5-5_medium_report | fixed | 40 | 39 | 39 | 2 | 0 | 40 | 40 |
