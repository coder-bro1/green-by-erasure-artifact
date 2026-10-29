### Table 1. Pre-repair signal and fates of bug-revealing tests (buggy condition)

| Model | Input | Signal units (of 20) | Generated tests | REVEALS | P1 dropped | P2 inverted | P2 neutralized | P2 dropped | P2 ENCODES created | P3 inverted | P3 neutralized | P3 dropped | P4 reported | P4 dropped |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-Coder 7B | code | 18 | 200 | 93 | 93 | 85 | 0 | 8 | 111 | 1 | 10 | 82 | 93 | 0 |
| Qwen2.5-Coder 7B | spec | 17 | 183 | 84 | 84 | 82 | 0 | 2 | 111 | 0 | 13 | 71 | 84 | 0 |
| Qwen3.5 9B | code | 12 | 190 | 51 | 51 | 44 | 0 | 7 | 69 | 0 | 32 | 19 | 39 | 12 |
| Qwen3.5 9B | spec | 11 | 169 | 51 | 51 | 45 | 1 | 5 | 55 | 0 | 29 | 22 | 40 | 11 |
| Gemma 4 12B | code | 15 | 212 | 83 | 83 | 78 | 0 | 5 | 98 | 0 | 16 | 67 | 83 | 0 |
| Gemma 4 12B | spec | 18 | 193 | 107 | 107 | 102 | 0 | 5 | 113 | 0 | 36 | 71 | 101 | 6 |

### Table 2. P4 triage with the v1 judge

| Model | Input | Quarantined on buggy | of which REVEALS | False alarms on fixed |
|---|---|---:|---:|---:|
| Qwen2.5-Coder 7B | code | 127 | 93 | 36 |
| Qwen2.5-Coder 7B | spec | 121 | 84 | 40 |
| Qwen3.5 9B | code | 70 | 39 | 15 |
| Qwen3.5 9B | spec | 49 | 40 | 10 |
| Gemma 4 12B | code | 103 | 83 | 10 |
| Gemma 4 12B | spec | 114 | 101 | 9 |

### Table 3. Fixed condition: final suite size and future-regression-revealing tests (REVEALS)

| Model | Input | GEN size / REVEALS | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|---|
| Qwen2.5-Coder 7B | code | 200 / 96 | 164 / 96 | 198 / 123 | 168 / 96 | 200 / 96 |
| Qwen2.5-Coder 7B | spec | 183 / 84 | 143 / 84 | 182 / 117 | 156 / 86 | 183 / 84 |
| Qwen3.5 9B | code | 192 / 87 | 159 / 87 | 192 / 110 | 167 / 94 | 174 / 87 |
| Qwen3.5 9B | spec | 169 / 51 | 134 / 51 | 168 / 62 | 140 / 54 | 144 / 51 |
| Gemma 4 12B | code | 194 / 113 | 180 / 113 | 194 / 126 | 186 / 113 | 190 / 113 |
| Gemma 4 12B | spec | 193 / 107 | 178 / 107 | 193 / 119 | 187 / 107 | 187 / 107 |

### Table 4. Change modes of erasures (classifier v2; a test can carry several modes)

| Model | Policy | Rewritten tests | Erasures | Modes of erasures |
|---|---|---:|---:|---|
| Qwen2.5-Coder 7B | P2 | 312 | 167 | EXPECTED_CHANGED 135, EXCEPTION_EXPECTED 26, TEST_REWRITTEN 6 |
| Qwen2.5-Coder 7B | P3 | 162 | 24 | FUNCTION_SHADOWED 23, TEST_REWRITTEN 1, INPUT_CHANGED 1, ASSERT_ADDED 1 |
| Qwen3.5 9B | P2 | 242 | 90 | EXPECTED_CHANGED 80, EXCEPTION_EXPECTED 5, TEST_REWRITTEN 4, INPUT_CHANGED 1 |
| Qwen3.5 9B | P3 | 178 | 61 | FUNCTION_SHADOWED 61, INPUT_CHANGED 1 |
| Gemma 4 12B | P2 | 245 | 180 | EXPECTED_CHANGED 147, EXCEPTION_EXPECTED 19, TEST_REWRITTEN 14 |
| Gemma 4 12B | P3 | 79 | 52 | FUNCTION_SHADOWED 52, INPUT_CHANGED 1, ASSERT_ADDED 1 |
