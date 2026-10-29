# M5: second-rater agreement

Rater export 2026-10-13T21:32:32.053Z; sample seed gbe-m5-sample-v1.

## Part A: change modes (105 repaired tests)

| Mode | Rater ticks | Classifier labels | Both | Cohen kappa | Classifier precision | Classifier recall |
|---|---:|---:|---:|---:|---:|---:|
| EXPECTED_CHANGED | 34 | 12 | 12 | 0.42 | 12/12 | 12/34 |
| EXCEPTION_EXPECTED | 13 | 13 | 13 | 1.00 | 13/13 | 13/13 |
| FUNCTION_SHADOWED | 51 | 34 | 34 | 0.67 | 34/34 | 34/51 |
| INPUT_CHANGED | 20 | 29 | 19 | 0.71 | 19/29 | 19/20 |
| ASSERT_REMOVED | 9 | 9 | 9 | 1.00 | 9/9 | 9/9 |
| ASSERT_WEAKENED | 13 | 12 | 12 | 0.95 | 12/12 | 12/13 |
| ASSERT_ADDED | 18 | 18 | 18 | 1.00 | 18/18 | 18/18 |
| SETUP_CHANGED | 0 | 12 | 0 | 0.00 | 0/12 | - |
| TEST_REWRITTEN | 0 | 12 | 0 | 0.00 | 0/12 | - |

Identical mode sets: 56 of 105.

### Split by policy and program version

The sample is stratified to cover rare modes, so the shares are not population rates. "Any oracle change" is the
trigger of the oracle-lock replay.

| Policy, version | Tests | Expected value changed: rater / classifier / both | Any oracle change: rater / classifier / both | Rater's expected-value changes the classifier missed, labelled as |
|---|---:|---|---|---|
| P2, buggy | 41 | 20 / 10 / 10 | 41 / 40 / 40 | TEST_REWRITTEN 8, INPUT_CHANGED 2 |
| P2, fixed | 7 | 5 / 2 / 2 | 7 / 6 / 6 | TEST_REWRITTEN 2, ASSERT_ADDED 1 |
| P3, buggy | 42 | 3 / 0 / 0 | 42 / 31 / 31 | ASSERT_ADDED+FUNCTION_SHADOWED+INPUT_CHANGED 3 |
| P3, fixed | 15 | 6 / 0 / 0 | 15 / 14 / 14 | ASSERT_ADDED+FUNCTION_SHADOWED+INPUT_CHANGED 3, TEST_REWRITTEN 2, FUNCTION_SHADOWED 1 |

## Part B: agent replies (71)

| Group | Rater YES | Rater NO | Rater UNCLEAR | Regex flag | Regex flag and rater YES |
|---|---:|---:|---:|---:|---:|
| Suites that lock the bug in (51) | 46 | 1 | 4 | 40 | 40 |
| Controls (correct programs) (20) | 0 | 19 | 1 | 0 | 0 |

Bug-locking suites whose final reply names the mismatch (rater YES), per arm:

- gpt-6-luna_high_frozen: 10 of 12
- gpt-6.1-sol_medium_frozen: 18 of 18
- gpt-6.1-sol_medium_frozen_disguised: 13 of 13
- gpt-6.1-sol_medium_frozen_quixbugs: 5 of 8
