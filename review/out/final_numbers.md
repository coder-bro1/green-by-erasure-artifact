# Final numbers with statistics (M2 to M4, M6; revised 18 October after the external review)

Computed by `analysis/final_numbers.py` after the time-out recheck. Brackets: 95% cluster-bootstrap
intervals over program pairs (2,000 resamples). Rates of bug-revealing tests are over all bug-revealing
tests of the buggy programs; P4 false reports over the failing tests of correct programs that the judge saw.

## RQ1 and RQ3 per run

### phase2_qwen25_code

Bug-revealing tests before repair: 868.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 93% [88, 97] | 0% [0, 0] | 7% [3, 12] | 0% [0, 0] |
| P3 | 1% [0, 1] | 17% [12, 21] | 83% [78, 87] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 23% [19, 27] | 77% [73, 81] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 42% [34, 50]; 144 of 341 judged failing tests (144 BUG, 0 UNSURE) among 2000 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 59% [53, 65] of those the judge saw (default judge: 77% [73, 81]); false reports 57% [49, 65]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 88% [82, 93], in erasures on buggy programs 88% [82, 93]
- Fix-blocking programs (of 204 buggy programs; 1 units of the run produced no test): discard 38, overwrite 187, free repair 46, triage 38; added by overwrite over discard 73% [67, 79] of buggy programs (discard: 19% [14, 24])
- Triage per program: bug reported for 86% [81, 91] of buggy programs (D, 176 of 204), at least one false report for 38% [31, 44] of correct programs (F, 77 of 204).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 4%; c = 0.25: p* = 10%; c = 0.5: p* = 18%; c = 1.0: p* = 30%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 17% [13, 22] with 13% [9, 18] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [99, 100]

### phase2_qwen35_code

Bug-revealing tests before repair: 759.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 90% [84, 94] | 0% [0, 1] | 10% [6, 15] | 0% [0, 0] |
| P3 | 1% [0, 1] | 48% [42, 55] | 51% [45, 58] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 6% [4, 9] | 94% [91, 96] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 43% [35, 51]; 115 of 270 judged failing tests (93 BUG, 22 UNSURE) among 2009 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 83% [78, 88] of those the judge saw (default judge: 94% [92, 96]); false reports 37% [29, 44]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 91% [86, 95], in erasures on buggy programs 84% [77, 90]
- Fix-blocking programs (of 204 buggy programs; 3 units of the run produced no test): discard 28, overwrite 156, free repair 30, triage 28; added by overwrite over discard 63% [56, 69] of buggy programs (discard: 14% [9, 19])
- Triage per program: bug reported for 75% [69, 81] of buggy programs (D, 154 of 204), at least one false report for 32% [26, 39] of correct programs (F, 66 of 204).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 4%; c = 0.25: p* = 10%; c = 0.5: p* = 18%; c = 1.0: p* = 30%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 49% [42, 55] with 30% [23, 38] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 99% [96, 100]

### phase2_gemma4_code

Bug-revealing tests before repair: 908.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 91% [86, 95] | 2% [1, 4] | 7% [3, 12] | 0% [0, 0] |
| P3 | 0% [0, 0] | 29% [25, 35] | 71% [65, 75] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 5% [3, 7] | 95% [93, 97] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 42% [31, 52]; 60 of 144 judged failing tests (54 BUG, 6 UNSURE) among 2054 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 91% [88, 94] of those the judge saw (default judge: 95% [93, 97]); false reports 43% [31, 54]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 90% [80, 96], in erasures on buggy programs 78% [70, 84]
- Fix-blocking programs (of 204 buggy programs; 1 units of the run produced no test): discard 56, overwrite 192, free repair 56, triage 56; added by overwrite over discard 67% [60, 73] of buggy programs (discard: 27% [22, 34])
- Triage per program: bug reported for 84% [78, 89] of buggy programs (D, 171 of 204), at least one false report for 18% [13, 24] of correct programs (F, 37 of 204).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 2%; c = 0.25: p* = 5%; c = 0.5: p* = 10%; c = 1.0: p* = 18%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 29% [25, 35] with 52% [40, 64] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

### phase2_qwen25_spec

Bug-revealing tests before repair: 818.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 94% [90, 98] | 0% [0, 0] | 6% [2, 10] | 0% [0, 0] |
| P3 | 1% [0, 4] | 17% [12, 21] | 82% [77, 86] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 26% [22, 30] | 74% [70, 78] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 45% [38, 52]; 174 of 387 judged failing tests (174 BUG, 0 UNSURE) among 1964 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 55% [49, 62] of those the judge saw (default judge: 74% [70, 78]); false reports 56% [48, 63]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 87% [80, 92], in erasures on buggy programs 88% [82, 94]
- Fix-blocking programs (of 204 buggy programs; 4 units of the run produced no test): discard 22, overwrite 167, free repair 30, triage 22; added by overwrite over discard 71% [65, 77] of buggy programs (discard: 11% [7, 15])
- Triage per program: bug reported for 77% [72, 82] of buggy programs (D, 157 of 204), at least one false report for 44% [37, 50] of correct programs (F, 89 of 204).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 5%; c = 0.25: p* = 12%; c = 0.5: p* = 22%; c = 1.0: p* = 36%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 18% [14, 23] with 18% [11, 24] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 98% [93, 100]

### phase2_qwen25_disguised

Bug-revealing tests before repair: 168.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 99% [96, 100] | 0% [0, 0] | 1% [0, 4] | 0% [0, 0] |
| P3 | 1% [0, 2] | 14% [5, 24] | 86% [75, 95] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 24% [15, 34] | 76% [66, 85] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 46% [31, 61]; 33 of 72 judged failing tests (33 BUG, 0 UNSURE) among 400 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 53% [40, 65] of those the judge saw (default judge: 76% [66, 85]); false reports 62% [48, 76]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 92% [81, 99], in erasures on buggy programs 100% [100, 100]
- Fix-blocking programs (of 40 buggy programs; 0 units of the run produced no test): discard 12, overwrite 38, free repair 13, triage 12; added by overwrite over discard 65% [50, 80] of buggy programs (discard: 30% [18, 45])
- Triage per program: bug reported for 90% [80, 98] of buggy programs (D, 36 of 40), at least one false report for 55% [40, 70] of correct programs (F, 22 of 40).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 6%; c = 0.25: p* = 13%; c = 0.5: p* = 23%; c = 1.0: p* = 38%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 14% [5, 25] with 6% [0, 14] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

### phase2_qwen35_disguised

Bug-revealing tests before repair: 125.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 90% [79, 98] | 0% [0, 0] | 10% [2, 21] | 0% [0, 0] |
| P3 | 0% [0, 0] | 54% [38, 68] | 46% [32, 62] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 6% [2, 11] | 94% [89, 98] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 45% [26, 67]; 17 of 38 judged failing tests (15 BUG, 2 UNSURE) among 399 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 83% [70, 94] of those the judge saw (default judge: 94% [89, 98]); false reports 55% [36, 78]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 86% [69, 97], in erasures on buggy programs 89% [78, 97]
- Fix-blocking programs (of 40 buggy programs; 1 units of the run produced no test): discard 12, overwrite 30, free repair 12, triage 12; added by overwrite over discard 45% [30, 62] of buggy programs (discard: 30% [15, 45])
- Triage per program: bug reported for 80% [68, 92] of buggy programs (D, 32 of 40), at least one false report for 30% [18, 45] of correct programs (F, 12 of 40).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 4%; c = 0.25: p* = 9%; c = 0.5: p* = 16%; c = 1.0: p* = 27%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 54% [38, 68] with 21% [10, 36] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 97% [90, 100]

### phase2_gemma4_disguised

Bug-revealing tests before repair: 152.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 97% [88, 100] | 0% [0, 0] | 3% [0, 12] | 0% [0, 0] |
| P3 | 0% [0, 0] | 34% [22, 45] | 66% [55, 78] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 3% [1, 7] | 97% [93, 99] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 48% [9, 79]; 13 of 27 judged failing tests (6 BUG, 7 UNSURE) among 408 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 92% [87, 97] of those the judge saw (default judge: 97% [93, 99]); false reports 52% [22, 74]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 96% [85, 100], in erasures on buggy programs 79% [62, 91]
- Fix-blocking programs (of 40 buggy programs; 0 units of the run produced no test): discard 12, overwrite 39, free repair 12, triage 12; added by overwrite over discard 68% [52, 82] of buggy programs (discard: 30% [15, 45])
- Triage per program: bug reported for 95% [88, 100] of buggy programs (D, 38 of 40), at least one false report for 12% [2, 22] of correct programs (F, 5 of 40).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 1%; c = 0.25: p* = 3%; c = 0.5: p* = 6%; c = 1.0: p* = 12%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 34% [22, 45] with 56% [42, 76] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

### phase2_qwen25_natural

Bug-revealing tests before repair: 9.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 100% [100, 100] | 0% [0, 0] | 0% [0, 0] | 0% [0, 0] |
| P3 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 22% [0, 50] | 78% [50, 100] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 60% [25, 83]; 18 of 30 judged failing tests (18 BUG, 0 UNSURE) among 241 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 100% [100, 100] of those the judge saw (default judge: 78% [50, 100]); false reports 67% [37, 87]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 100% [100, 100], in erasures on buggy programs 100% [100, 100]
- Fix-blocking programs (of 25 buggy programs; 1 units of the run produced no test): discard 3, overwrite 11, free repair 3, triage 3; added by overwrite over discard 32% [16, 52] of buggy programs (discard: 12% [0, 28])
- Triage per program: bug reported for 28% [12, 48] of buggy programs (D, 7 of 25), at least one false report for 28% [12, 44] of correct programs (F, 7 of 25).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 9%; c = 0.25: p* = 20%; c = 0.5: p* = 33%; c = 1.0: p* = 50%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 0% [0, 0] with 3% [0, 11] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

### phase2_qwen35_natural

Bug-revealing tests before repair: 11.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 73% [43, 100] | 0% [0, 0] | 27% [0, 57] | 0% [0, 0] |
| P3 | 0% [0, 0] | 18% [0, 40] | 82% [60, 100] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 18% [0, 40] | 82% [60, 100] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 44% [25, 66]; 14 of 32 judged failing tests (11 BUG, 3 UNSURE) among 251 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 73% [42, 100] of those the judge saw (default judge: 82% [60, 100]); false reports 47% [29, 67]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 84% [63, 97], in erasures on buggy programs 100% [100, 100]
- Fix-blocking programs (of 25 buggy programs; 0 units of the run produced no test): discard 2, overwrite 9, free repair 2, triage 2; added by overwrite over discard 28% [12, 48] of buggy programs (discard: 8% [0, 20])
- Triage per program: bug reported for 36% [16, 56] of buggy programs (D, 9 of 25), at least one false report for 44% [24, 64] of correct programs (F, 11 of 25).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 11%; c = 0.25: p* = 23%; c = 0.5: p* = 38%; c = 1.0: p* = 55%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 18% [0, 40] with 12% [3, 23] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

### phase2_gemma4_natural

Bug-revealing tests before repair: 17.

| Policy | Inverted | Neutralized | Dropped | Reported |
|---|---|---|---|---|
| P1 | 0% [0, 0] | 0% [0, 0] | 100% [100, 100] | 0% [0, 0] |
| P2 | 100% [100, 100] | 0% [0, 0] | 0% [0, 0] | 0% [0, 0] |
| P3 | 0% [0, 0] | 24% [0, 47] | 76% [53, 100] | 0% [0, 0] |
| P4 | 0% [0, 0] | 0% [0, 0] | 18% [0, 33] | 82% [67, 100] |

- P4 false reports (failing tests of correct programs that the judge does not call wrong): 50% [20, 75]; 8 of 16 judged failing tests (8 BUG, 0 UNSURE) among 252 tests on correct programs
- Judge that also sees the code (D10): bug-revealing tests kept 82% [58, 100] of those the judge saw (default judge: 82% [67, 100]); false reports 50% [20, 75]
- Same edit under overwrite: expected value changed in repairs of wrong tests on correct programs 62% [27, 89], in erasures on buggy programs 82% [55, 100]
- Fix-blocking programs (of 25 buggy programs; 1 units of the run produced no test): discard 6, overwrite 15, free repair 6, triage 6; added by overwrite over discard 36% [20, 56] of buggy programs (discard: 24% [8, 40])
- Triage per program: bug reported for 40% [20, 60] of buggy programs (D, 10 of 25), at least one false report for 24% [8, 40] of correct programs (F, 6 of 25).
- Decision rule, triage beats overwrite above a share p* of buggy programs: c = 0.1: p* = 6%; c = 0.25: p* = 13%; c = 0.5: p* = 23%; c = 1.0: p* = 38%.
- Oracle lock replayed on free repair (classifier-based; under free repair the classifier finds an oracle change in 31 of 42 rater-confirmed cases, so both figures are underestimates; discussion only): unrepairable tests dropped, evidence kept 24% [0, 47] with 56% [25, 83] of correct-program failures reported; unrepairable tests reported, 100% [100, 100] with 100% [100, 100]

## Triage outside the 20 pilot programs (the judge prompt was chosen on their Phase 1 replays)

| Run | Pairs | Revealing tests reported | False reports (failing tests of correct programs) | D | F |
|---|---:|---|---|---|---|
| phase2_qwen25_code | 184 | 78% [74, 82] | 44% [36, 52] | 86% [80, 91] | 39% [32, 46] |
| phase2_qwen35_code | 184 | 94% [91, 96] | 42% [34, 51] | 78% [72, 84] | 33% [27, 40] |
| phase2_gemma4_code | 184 | 95% [92, 97] | 42% [32, 54] | 85% [79, 90] | 18% [13, 24] |

## RQ2 (visibility): paired metric differences, overwrite minus discard, buggy programs

Overwrite keeps every test discard keeps, unchanged, so no difference can be negative; the rows give the size.

| Run | Units | Mutation score | Line coverage (green) | Branch coverage (green) | Line coverage (all tests) |
|---|---:|---|---|---|---|
| phase2_qwen25_code | 204 | +28.6 pts [+24.0, +33.7] | +14.5 pts [+11.2, +18.2] | +24.7 pts [+19.5, +30.2] | +14.6 pts [+11.2, +18.3] |
| phase2_qwen35_code | 204 | +23.1 pts [+18.6, +27.8] | +11.0 pts [+8.3, +14.1] | +19.1 pts [+14.4, +23.9] | +11.1 pts [+8.3, +14.2] |
| phase2_gemma4_code | 204 | +22.1 pts [+18.2, +26.5] | +12.4 pts [+9.3, +15.6] | +22.1 pts [+17.1, +27.7] | +12.4 pts [+9.4, +15.6] |
| phase2_qwen25_spec | 204 | +28.4 pts [+23.5, +33.6] | +14.0 pts [+10.8, +17.6] | +23.8 pts [+18.7, +29.2] | +14.1 pts [+10.8, +17.6] |
| phase2_qwen25_disguised | 40 | +30.8 pts [+21.7, +40.5] | +11.9 pts [+4.9, +19.7] | +22.0 pts [+10.5, +34.8] | +11.9 pts [+4.9, +19.7] |
| phase2_qwen35_disguised | 40 | +20.9 pts [+11.7, +31.4] | +10.0 pts [+3.8, +17.8] | +15.6 pts [+6.4, +26.7] | +10.0 pts [+3.8, +17.8] |
| phase2_gemma4_disguised | 40 | +23.4 pts [+15.3, +32.2] | +6.8 pts [+2.9, +11.5] | +15.2 pts [+7.7, +23.8] | +6.8 pts [+2.9, +11.5] |
| phase2_qwen25_natural | 25 | +6.3 pts [+0.9, +15.4] | +2.4 pts [+0.0, +6.7] | +0.6 pts [+0.0, +2.0] | +2.4 pts [+0.0, +6.7] |

## Seed spread (Qwen2.5, 40 pairs, temperature 0.8, seeds 1 to 3; temperature-0 code run on the same pairs)

| Run | Revealing tests | Overwrite: inverted | Free repair: kept revealing | Triage: reported |
|---|---:|---:|---:|---:|
| phase2_qwen25_code | 157 | 153 (97%) | 0 | 120 (76%) |
| phase2_qwen25_seed1 | 153 | 149 (97%) | 0 | 109 (71%) |
| phase2_qwen25_seed2 | 155 | 154 (99%) | 0 | 109 (70%) |
| phase2_qwen25_seed3 | 157 | 152 (97%) | 0 | 125 (80%) |

