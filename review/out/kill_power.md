# RQ2: kill power of the tests overwrite adds

Computed by `analysis/kill_power.py` from the kill matrices. Shares of the mutants of the version; means over
added green tests with 95% cluster-bootstrap intervals over pairs. Marginal: killed by the added test and not by
the discard suite of its unit.

| Run | Added tests | Tests | Mutants killed per test | Marginal kills per test |
|---|---|---:|---|---|
| phase2_qwen25_code | buggy: inverted revealing tests (fault-enforcing) | 754 | 60.1% [54.9, 65.1] | 32.5% [27.4, 37.9] |
| phase2_qwen25_code | buggy: inverted by a copy rule | 753 | 60.1% [54.9, 65.2] | 32.6% [27.4, 38.0] |
| phase2_qwen25_code | buggy: inverted by the model | 1 | 42.9% [42.9, 42.9] | 7.1% [7.1, 7.1] |
| phase2_qwen25_code | buggy: other added tests | 274 | 61.0% [54.2, 67.2] | 26.8% [19.7, 33.7] |
| phase2_qwen25_code | correct: repairs of wrong tests | 309 | 66.8% [61.1, 72.3] | 4.5% [1.6, 8.3] |
| phase2_qwen35_code | buggy: inverted revealing tests (fault-enforcing) | 648 | 56.9% [51.8, 62.2] | 32.0% [26.3, 37.9] |
| phase2_qwen35_code | buggy: inverted by a copy rule | 616 | 57.7% [52.0, 63.3] | 32.1% [26.0, 37.7] |
| phase2_qwen35_code | buggy: inverted by the model | 32 | 41.8% [33.0, 53.3] | 28.9% [14.5, 41.2] |
| phase2_qwen35_code | buggy: other added tests | 363 | 32.5% [24.1, 42.1] | 11.6% [7.3, 16.8] |
| phase2_qwen35_code | correct: repairs of wrong tests | 242 | 58.6% [49.9, 66.7] | 2.1% [1.0, 3.5] |
| phase2_gemma4_code | buggy: inverted revealing tests (fault-enforcing) | 781 | 57.9% [52.8, 62.9] | 29.3% [24.2, 34.6] |
| phase2_gemma4_code | buggy: inverted by a copy rule | 692 | 59.3% [54.2, 64.5] | 30.6% [25.2, 36.2] |
| phase2_gemma4_code | buggy: inverted by the model | 89 | 47.1% [41.1, 53.4] | 19.0% [10.8, 26.8] |
| phase2_gemma4_code | buggy: other added tests | 139 | 52.5% [39.9, 65.8] | 9.8% [5.3, 15.6] |
| phase2_gemma4_code | correct: repairs of wrong tests | 132 | 69.6% [62.3, 76.1] | 1.3% [0.4, 2.4] |
| phase2_qwen25_spec | buggy: inverted revealing tests (fault-enforcing) | 709 | 58.8% [53.5, 63.8] | 35.2% [29.5, 40.8] |
| phase2_qwen25_spec | buggy: inverted by a copy rule | 709 | 58.8% [53.5, 63.8] | 35.2% [29.5, 40.8] |
| phase2_qwen25_spec | buggy: other added tests | 294 | 53.2% [45.2, 61.1] | 22.4% [15.6, 29.6] |
| phase2_qwen25_spec | correct: repairs of wrong tests | 339 | 59.3% [51.9, 66.5] | 7.3% [2.9, 12.7] |
| phase2_qwen25_disguised | buggy: inverted revealing tests (fault-enforcing) | 163 | 59.5% [50.2, 68.8] | 33.0% [20.4, 44.5] |
| phase2_qwen25_disguised | buggy: inverted by a copy rule | 163 | 59.5% [50.2, 68.8] | 33.0% [20.4, 44.5] |
| phase2_qwen25_disguised | buggy: other added tests | 59 | 64.1% [51.3, 75.4] | 21.7% [11.3, 31.5] |
| phase2_qwen25_disguised | correct: repairs of wrong tests | 71 | 60.5% [48.5, 70.7] | 6.6% [0.6, 13.1] |
| phase2_qwen35_disguised | buggy: inverted revealing tests (fault-enforcing) | 108 | 62.2% [52.9, 70.5] | 33.2% [19.1, 44.3] |
| phase2_qwen35_disguised | buggy: inverted by a copy rule | 96 | 65.4% [56.3, 74.0] | 36.7% [22.5, 48.4] |
| phase2_qwen35_disguised | buggy: inverted by the model | 12 | 36.7% [25.0, 46.5] | 5.2% [1.0, 11.5] |
| phase2_qwen35_disguised | buggy: other added tests | 68 | 45.7% [26.1, 68.6] | 24.8% [11.0, 41.3] |
| phase2_qwen35_disguised | correct: repairs of wrong tests | 35 | 53.4% [38.6, 69.1] | 1.5% [0.0, 3.2] |
| phase2_gemma4_disguised | buggy: inverted revealing tests (fault-enforcing) | 140 | 62.0% [51.1, 71.1] | 29.9% [17.6, 40.0] |
| phase2_gemma4_disguised | buggy: inverted by a copy rule | 109 | 68.0% [56.2, 78.4] | 33.6% [19.0, 46.1] |
| phase2_gemma4_disguised | buggy: inverted by the model | 31 | 40.9% [33.1, 45.9] | 16.8% [2.7, 27.4] |
| phase2_gemma4_disguised | buggy: other added tests | 16 | 66.4% [49.5, 79.7] | 19.2% [9.1, 28.8] |
| phase2_gemma4_disguised | correct: repairs of wrong tests | 27 | 69.6% [53.6, 79.6] | 0.9% [0.0, 1.8] |

## The inverted tests and the rise (buggy programs)

Mean mutation score over buggy units with mutants. Reproduced: (discard + inverted - discard) / (overwrite -
discard). Lost on removal: (overwrite - overwrite without inverted) / (overwrite - discard). Kills overlap, so
the two shares are different estimands, not a decomposition.

| Run | Units | Discard | Discard plus inverted tests | Overwrite without inverted tests | Overwrite | Reproduced by adding inverted tests | Lost on removing them |
|---|---:|---:|---:|---:|---:|---:|---:|
| phase2_qwen25_code | 190 | 50.2% | 76.2% | 66.6% | 78.8% | 91% | 43% |
| phase2_qwen35_code | 190 | 44.6% | 66.2% | 55.5% | 67.7% | 94% | 52% |
| phase2_gemma4_code | 190 | 57.8% | 79.0% | 62.3% | 80.0% | 96% | 80% |
| phase2_qwen25_spec | 190 | 40.7% | 66.0% | 55.8% | 69.0% | 89% | 47% |
| phase2_qwen25_disguised | 38 | 54.3% | 82.0% | 65.9% | 85.1% | 90% | 62% |
| phase2_qwen35_disguised | 38 | 52.7% | 72.5% | 68.2% | 73.6% | 95% | 26% |
| phase2_gemma4_disguised | 38 | 64.1% | 85.8% | 68.9% | 87.4% | 93% | 79% |

## The rise from discard to overwrite on buggy and correct programs

Mean mutation score over units with mutants, and the rise from discard to overwrite (points of mutation
score) with 95% cluster-bootstrap intervals over pairs. Added: green tests per unit that overwrite keeps and
discard does not. Remaining caught: of the mutants the discard suite misses, the share the overwrite suite
kills (pooled over units, so the rise is set against the room left for it). Paired: rise on the buggy
version minus rise on the fixed version of the same pair, over pairs whose two versions both have mutants.

| Run | Version | Units | Added tests per unit | Discard | Overwrite | Rise | Remaining caught | Paired: buggy minus correct |
|---|---|---:|---:|---:|---:|---|---|---|
| phase2_qwen25_code | buggy | 190 | 5.4 | 50.2% | 78.8% | 28.6% [24.1, 33.4] | 56% [47, 64] | 26.2% [21.5, 31.2] |
| phase2_qwen25_code | correct | 194 | 1.6 | 87.5% | 90.0% | 2.5% [1.2, 4.1] | 26% [13, 39] |  |
| phase2_qwen35_code | buggy | 190 | 5.3 | 44.6% | 67.7% | 23.1% [18.8, 27.6] | 46% [37, 55] | 21.3% [16.8, 26.0] |
| phase2_qwen35_code | correct | 194 | 1.2 | 76.3% | 78.1% | 1.8% [0.8, 3.2] | 16% [5, 31] |  |
| phase2_gemma4_code | buggy | 190 | 4.8 | 57.8% | 80.0% | 22.1% [18.1, 26.3] | 49% [40, 59] | 21.7% [17.7, 26.0] |
| phase2_gemma4_code | correct | 194 | 0.7 | 90.5% | 91.0% | 0.5% [0.2, 0.9] | 5% [2, 9] |  |
| phase2_qwen25_spec | buggy | 190 | 5.3 | 40.7% | 69.0% | 28.4% [23.7, 33.1] | 41% [33, 50] | 24.2% [19.2, 29.4] |
| phase2_qwen25_spec | correct | 194 | 1.7 | 76.4% | 80.1% | 3.6% [1.8, 5.8] | 15% [7, 25] |  |
| phase2_qwen25_disguised | buggy | 38 | 5.8 | 54.3% | 85.1% | 30.8% [21.2, 40.9] | 66% [48, 81] | 27.7% [17.9, 38.7] |
| phase2_qwen25_disguised | correct | 39 | 1.8 | 86.4% | 89.4% | 3.0% [0.6, 6.1] | 29% [5, 49] |  |
| phase2_qwen35_disguised | buggy | 38 | 4.6 | 52.7% | 73.6% | 20.9% [11.7, 31.3] | 51% [28, 73] | 20.1% [11.0, 30.3] |
| phase2_qwen35_disguised | correct | 39 | 0.9 | 73.8% | 75.1% | 1.3% [0.0, 3.4] | 8% [0, 21] |  |
| phase2_gemma4_disguised | buggy | 38 | 4.1 | 64.1% | 87.4% | 23.4% [14.9, 32.2] | 62% [43, 77] | 23.1% [14.7, 31.9] |
| phase2_gemma4_disguised | correct | 39 | 0.7 | 92.9% | 93.2% | 0.2% [0.0, 0.6] | 5% [0, 12] |  |
