# C1 section 10: developers' bug-revealing tests through the four policies

Run `c1_devtests_qwen25_r2` (Qwen2.5-Coder 7B, the study run's prompts and policies; suites seeded with the
developers' tests by `analysis/c1_devtests.py`; environment warm-up of change 8; 30 s recheck applied, 2 tests).
10 tests in 8 bugs, every one revealing before repair (fails on buggy, passes on fixed, twice each). On the fixed
versions every test passes and every policy keeps it (no false report is possible).

| Bug | First outcome on buggy | Discard | Overwrite | Free repair | Triage |
|---|---|---|---|---|---|
| httpie-4 | assertion failure (literal expected) | dropped | inverted in one step (T3: expected value set to the observed one) | dropped (shadowed the function) | dropped (judge: test wrong) |
| spacy-2 | assertion failure (literal expected) | dropped | inverted in one step (T3) | dropped (shadowed, input changed) | dropped (judge: test wrong) |
| pandas-23 (2 tests) | assertion failure (non-literal expected) | dropped | dropped (3 model rewrites still fail) | dropped (shadowed) | reported (judge: bug) |
| pandas-168 | exception in pandas | dropped | dropped (T4 wrap, then the test breaks) | dropped (shadowed) | reported (judge: bug) |
| pandas-58 test 1 | exception in pandas | dropped | dropped (T4 wrap, then unparseable rewrites) | dropped | reported (judge: bug) |
| pandas-58 test 2 | test error (`pytest.raises` pattern mismatch) | dropped | dropped (unparseable rewrites) | dropped | dropped (not judged: test error) |
| pandas-127 | exception in pandas | dropped | dropped (T4 wrap, then broken) | dropped (shadowed) | dropped (judge: test wrong) |
| pandas-162 | exception in pandas | dropped | dropped (T4 wrap, then broken) | dropped (shadowed, input changed) | dropped (judge: test wrong) |
| pandas-161 | test error (assertion inside a pandas helper) | dropped | dropped (unparseable rewrites) | dropped | dropped (not judged: test error) |

Totals over 10 tests: discard drops 10; overwrite inverts 2 and drops 8; free repair drops 10 (7 rewrites
replaced the function under test with a local copy); triage reports 4 and drops 6 (4 judged wrong, 2 test errors
it never judges). Fault-enforcing bugs: overwrite 2 of 8 (httpie-4, spacy-2), every other policy 0.

Reading: overwrite inverts a developer's revealing test exactly where the edit is mechanical (an assertion with a
literal expected value: 2 of 2). Where the expected value is an object or the failure is an exception raised deep
in pandas, the 7B repairer cannot produce a passing test and the evidence is dropped instead. No policy except
triage keeps evidence, and triage keeps it for 4 of 10 tests. Superseded run `c1_devtests_qwen25`: 4 tests timed
out at first execution (cold start) and are not reported (change 8).
