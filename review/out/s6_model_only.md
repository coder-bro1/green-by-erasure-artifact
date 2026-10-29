# S6: overwrite with and without its copy rules

Computed by `analysis/s6_summary.py`. P2: overwrite as in the main runs (copy rules first, model when none
applies). P2M: the same generated tests with the rules off, every repair by the model with overwrite's prompt.
Shares with 95% cluster-bootstrap intervals over pairs.


## Fates of the bug-revealing tests and fault-enforcing suites (buggy units)

| Run | Inversions by rule (P2) | Inversions by model (P2) | Policy | Revealing tests | Inverted | Neutralized | Dropped | Suites asserting the bug |
|---|---:|---:|---|---:|---|---|---|---|
| s6_model_only_gemma4 | 737 | 89 | P2 | 908 | 91% [86, 95] | 2% [1, 4] | 7% [3, 11] | 94% [91, 97] |
| s6_model_only_gemma4 | 737 | 89 | P2M | 908 | 76% [69, 82] | 10% [6, 13] | 15% [10, 20] | 89% [85, 93] |
| s6_model_only_qwen25 | 805 | 1 | P2 | 868 | 93% [88, 97] | 0% [0, 0] | 7% [3, 12] | 92% [88, 95] |
| s6_model_only_qwen25 | 805 | 1 | P2M | 868 | 9% [6, 13] | 4% [2, 7] | 87% [83, 90] | 42% [35, 49] |

## Mutation score (units with mutants)

Remaining caught: of the mutants the discard suite misses, the share the policy's suite kills (pooled).
Paired: P2M rise on the buggy version minus on the fixed version of the same pair. Plus inverted: the
discard suite plus only the P2M inverted tests. Per test: mutants killed by one P2M inverted test.

| Run | Version | Units | Discard | P2 | P2M | P2M rise | Remaining caught (P2M) | Paired | Plus inverted | Per inverted test | Mutant hash mismatches |
|---|---|---:|---:|---:|---:|---|---|---|---:|---|---:|
| s6_model_only_gemma4 | buggy | 190 | 57.8% | 80.0% | 78.9% | 21.1% [17.2, 25.1] | 47% [38, 57] | 20.7% [16.6, 24.8] | 77.9% | 59.1% [54.3, 64.3] | 0 |
| s6_model_only_gemma4 | correct | 194 | 90.5% | 91.0% | 91.0% | 0.5% [0.2, 0.9] | 5% [2, 9] |  |  |  | 0 |
| s6_model_only_qwen25 | buggy | 190 | 50.2% | 78.8% | 61.6% | 11.4% [8.0, 15.1] | 24% [16, 34] | 10.5% [7.0, 14.2] | 58.2% | 73.3% [63.2, 82.0] | 0 |
| s6_model_only_qwen25 | correct | 194 | 87.5% | 90.0% | 88.4% | 1.0% [0.4, 1.7] | 11% [3, 19] |  |  |  | 0 |
