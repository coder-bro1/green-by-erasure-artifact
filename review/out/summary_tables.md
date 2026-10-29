# Summary tables (Phase 2)

Computed by `analysis/summary_tables.py` after the time-out recheck.

## Table 1. Fault enforcement: fate of bug-revealing tests and fix-blocking programs (RQ1)

Shares of the bug-revealing tests generated for buggy programs; 95% cluster-bootstrap intervals over program pairs.
Discard (P1), overwrite (P2) and free repair (P3) keep only tests that pass on the buggy program, so none keeps a
revealing test (a property of the design). Fix-blocking: buggy programs whose final suite keeps a test that passes
on the bug and fails on the fix; programs counted over the whole design, including units without tests. Every test
P1 keeps is kept by P2 to P4, so the policies can only add fix-blocking programs to P1.

| Model | Programs | Pairs | Revealing tests | Overwrite: inverted | Free repair: neutralized | Triage: reported | Triage: false reports | Fix-blocking programs, discard / overwrite / free repair / triage | Added by overwrite |
|---|---|---:|---:|---|---|---|---|---|---|
| Qwen2.5-Coder 7B | HumanEvalFix | 204 | 868 | 93% [88, 97] | 17% [12, 21] | 77% [73, 81] | 42% [34, 50] | 38 / 187 / 46 / 38 of 204 | 73% [67, 79] |
| Qwen3.5 9B | HumanEvalFix | 204 | 759 | 90% [84, 94] | 48% [42, 55] | 94% [91, 96] | 43% [35, 51] | 28 / 156 / 30 / 28 of 204 | 63% [56, 69] |
| Gemma 4 12B | HumanEvalFix | 204 | 908 | 91% [86, 95] | 29% [25, 35] | 95% [93, 97] | 42% [31, 52] | 56 / 192 / 56 / 56 of 204 | 67% [60, 73] |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | 204 | 818 | 94% [90, 98] | 17% [12, 21] | 74% [70, 78] | 45% [38, 52] | 22 / 167 / 30 / 22 of 204 | 71% [65, 77] |
| Qwen2.5-Coder 7B | disguised | 40 | 168 | 99% [96, 100] | 14% [5, 24] | 76% [66, 85] | 46% [31, 61] | 12 / 38 / 13 / 12 of 40 | 65% [50, 80] |
| Qwen3.5 9B | disguised | 40 | 125 | 90% [79, 98] | 54% [38, 68] | 94% [89, 98] | 45% [26, 67] | 12 / 30 / 12 / 12 of 40 | 45% [30, 62] |
| Gemma 4 12B | disguised | 40 | 152 | 97% [88, 100] | 34% [22, 45] | 97% [93, 99] | 48% [9, 79] | 12 / 39 / 12 / 12 of 40 | 68% [52, 82] |
| Qwen2.5-Coder 7B | natural faults | 25 | 9 | 100% [100, 100] | 0% [0, 0] | 78% [50, 100] | 60% [25, 83] | 3 / 11 / 3 / 3 of 25 | 32% [16, 52] |
| Qwen3.5 9B | natural faults | 25 | 11 | 73% [43, 100] | 18% [0, 40] | 82% [60, 100] | 44% [25, 66] | 2 / 9 / 2 / 2 of 25 | 28% [12, 48] |
| Gemma 4 12B | natural faults | 25 | 17 | 100% [100, 100] | 24% [0, 47] | 82% [67, 100] | 50% [20, 75] | 6 / 15 / 6 / 6 of 25 | 36% [20, 56] |

## Table 2. What the metrics show beside what the suite keeps (RQ2, buggy programs)

Means over all buggy programs of the design (an empty suite scores 0) on the version the pipeline ran on; coverage of
the green tests. Evidence: the suite holds or reports a test that reveals the bug. P2 to P4 keep every P1 test, so
they cannot score lower than P1. Paired differences with intervals are in final_numbers.md, kill power in
kill_power.md.

| Model | Programs | Suite | Mutation score | Line coverage | Branch coverage | Bug evidence | Fix-blocking |
|---|---|---|---:|---:|---:|---:|---:|
| Qwen2.5-Coder 7B | HumanEvalFix | generated, before repair | 50.2% | 57.3% | 64.6% | 90% | 19% |
| Qwen2.5-Coder 7B | HumanEvalFix | discard | 50.2% | 57.3% | 64.6% | 0% | 19% |
| Qwen2.5-Coder 7B | HumanEvalFix | overwrite | 78.8% | 71.8% | 89.4% | 0% | 92% |
| Qwen2.5-Coder 7B | HumanEvalFix | free repair | 52.4% | 58.3% | 65.4% | 0% | 23% |
| Qwen2.5-Coder 7B | HumanEvalFix | triage | 50.2% | 57.3% | 64.6% | 86% | 19% |
| Qwen3.5 9B | HumanEvalFix | generated, before repair | 44.6% | 51.6% | 61.2% | 76% | 14% |
| Qwen3.5 9B | HumanEvalFix | discard | 44.6% | 51.6% | 61.2% | 0% | 14% |
| Qwen3.5 9B | HumanEvalFix | overwrite | 67.7% | 62.6% | 80.3% | 0% | 76% |
| Qwen3.5 9B | HumanEvalFix | free repair | 46.3% | 52.5% | 61.9% | 0% | 15% |
| Qwen3.5 9B | HumanEvalFix | triage | 44.6% | 51.6% | 61.2% | 75% | 14% |
| Gemma 4 12B | HumanEvalFix | generated, before repair | 57.8% | 60.7% | 68.7% | 84% | 27% |
| Gemma 4 12B | HumanEvalFix | discard | 57.8% | 60.7% | 68.7% | 0% | 27% |
| Gemma 4 12B | HumanEvalFix | overwrite | 80.0% | 73.0% | 90.8% | 0% | 94% |
| Gemma 4 12B | HumanEvalFix | free repair | 57.8% | 60.7% | 68.7% | 0% | 27% |
| Gemma 4 12B | HumanEvalFix | triage | 57.8% | 60.7% | 68.7% | 84% | 27% |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | generated, before repair | 40.7% | 49.2% | 53.3% | 80% | 11% |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | discard | 40.7% | 49.2% | 53.3% | 0% | 11% |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | overwrite | 69.0% | 63.2% | 77.1% | 0% | 82% |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | free repair | 43.0% | 50.1% | 54.3% | 0% | 15% |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | triage | 40.7% | 49.2% | 53.3% | 77% | 11% |
| Qwen2.5-Coder 7B | disguised | generated, before repair | 54.3% | 64.5% | 73.9% | 90% | 30% |
| Qwen2.5-Coder 7B | disguised | discard | 54.3% | 64.5% | 73.9% | 0% | 30% |
| Qwen2.5-Coder 7B | disguised | overwrite | 85.1% | 76.4% | 95.9% | 0% | 95% |
| Qwen2.5-Coder 7B | disguised | free repair | 55.5% | 65.7% | 75.5% | 0% | 32% |
| Qwen2.5-Coder 7B | disguised | triage | 54.3% | 64.5% | 73.9% | 90% | 30% |
| Qwen3.5 9B | disguised | generated, before repair | 52.7% | 55.8% | 65.3% | 80% | 30% |
| Qwen3.5 9B | disguised | discard | 52.7% | 55.8% | 65.3% | 0% | 30% |
| Qwen3.5 9B | disguised | overwrite | 73.6% | 65.8% | 80.9% | 0% | 75% |
| Qwen3.5 9B | disguised | free repair | 54.4% | 55.8% | 65.3% | 0% | 30% |
| Qwen3.5 9B | disguised | triage | 52.7% | 55.8% | 65.3% | 80% | 30% |
| Gemma 4 12B | disguised | generated, before repair | 64.1% | 70.3% | 81.8% | 95% | 30% |
| Gemma 4 12B | disguised | discard | 64.1% | 70.3% | 81.8% | 0% | 30% |
| Gemma 4 12B | disguised | overwrite | 87.4% | 77.1% | 97.0% | 0% | 98% |
| Gemma 4 12B | disguised | free repair | 64.1% | 70.3% | 81.8% | 0% | 30% |
| Gemma 4 12B | disguised | triage | 64.1% | 70.3% | 81.8% | 95% | 30% |
| Qwen2.5-Coder 7B | natural faults | generated, before repair | 68.3% | 69.8% | 86.7% | 32% | 12% |
| Qwen2.5-Coder 7B | natural faults | discard | 68.3% | 69.8% | 86.7% | 0% | 12% |
| Qwen2.5-Coder 7B | natural faults | overwrite | 74.6% | 72.2% | 87.3% | 0% | 44% |
| Qwen2.5-Coder 7B | natural faults | free repair | 68.3% | 69.8% | 86.7% | 0% | 12% |
| Qwen2.5-Coder 7B | natural faults | triage | 68.3% | 69.8% | 86.7% | 28% | 12% |

## Table 3. The price of preservation (RQ3)

D: buggy programs whose bug triage reports. F: correct programs with at least one false report; both over the whole
design, with cluster-bootstrap intervals. Held-out pairs (outside the judge's 20 pilot programs) in final_numbers.md. Triage beats
overwrite when the share of buggy programs exceeds p* = cF / (D + cF), c the cost of a false report relative to
a missed bug. Judge with code: the same tests judged with the program source in the prompt (D10).

| Model | Programs | D | F | p* at c = 0.25 | p* at c = 0.5 | p* at c = 1 | Judge with code: revealing tests reported | Judge with code: false reports |
|---|---|---|---|---:|---:|---:|---|---|
| Qwen2.5-Coder 7B | HumanEvalFix | 86% [81, 91] | 38% [31, 44] | 10% | 18% | 30% | 59% [53, 65] | 57% [49, 65] |
| Qwen3.5 9B | HumanEvalFix | 75% [69, 81] | 32% [26, 39] | 10% | 18% | 30% | 83% [78, 88] | 37% [29, 44] |
| Gemma 4 12B | HumanEvalFix | 84% [78, 89] | 18% [13, 24] | 5% | 10% | 18% | 91% [88, 94] | 43% [31, 54] |
| Qwen2.5-Coder 7B | HumanEvalFix, spec in prompt | 77% [72, 82] | 44% [37, 50] | 12% | 22% | 36% | 55% [49, 62] | 56% [48, 63] |
| Qwen2.5-Coder 7B | disguised | 90% [80, 98] | 55% [40, 70] | 13% | 23% | 38% | 53% [40, 65] | 62% [48, 76] |
| Qwen3.5 9B | disguised | 80% [68, 92] | 30% [18, 45] | 9% | 16% | 27% | 83% [70, 94] | 55% [36, 78] |
| Gemma 4 12B | disguised | 95% [88, 100] | 12% [2, 22] | 3% | 6% | 12% | 92% [87, 97] | 52% [22, 74] |
| Qwen2.5-Coder 7B | natural faults | 28% [12, 48] | 28% [12, 44] | 20% | 33% | 50% | 100% [100, 100] | 67% [37, 87] |
| Qwen3.5 9B | natural faults | 36% [16, 56] | 44% [24, 64] | 23% | 38% | 55% | 73% [42, 100] | 47% [29, 67] |
| Gemma 4 12B | natural faults | 40% [20, 60] | 24% [8, 40] | 13% | 23% | 38% | 82% [58, 100] | 50% [20, 75] |

## Table 4. The judge under weaker specifications (S4)

Judge replayed on the same failing tests with the full docstring, without its examples, or with the signature only.
Kept: a bug-revealing test of a buggy program is reported (BUG or UNSURE).

| Model | Specification | Bug-revealing tests reported | False reports on correct programs | UNSURE verdicts |
|---|---|---|---|---:|
| Qwen2.5-Coder 7B | full docstring | 668 of 868 (77%) | 144 of 341 (42%) | 1 |
| Qwen2.5-Coder 7B | no examples | 705 of 868 (81%) | 174 of 341 (51%) | 0 |
| Qwen2.5-Coder 7B | signature only | 531 of 868 (61%) | 153 of 341 (45%) | 0 |
| Qwen3.5 9B | full docstring | 711 of 759 (94%) | 115 of 270 (43%) | 65 |
| Qwen3.5 9B | no examples | 653 of 759 (86%) | 110 of 270 (41%) | 97 |
| Qwen3.5 9B | signature only | 719 of 759 (95%) | 236 of 270 (87%) | 1074 |
| Gemma 4 12B | full docstring | 863 of 908 (95%) | 60 of 144 (42%) | 40 |
| Gemma 4 12B | no examples | 853 of 908 (94%) | 60 of 144 (42%) | 92 |
| Gemma 4 12B | signature only | 894 of 908 (98%) | 136 of 144 (94%) | 1048 |

## Table 5. Coding agents asked to make failing tests pass with the code frozen (RQ4, arm A)

40 buggy programs per row. Each final suite is run against the original fixed and buggy programs. Reveals
(diagnostic): a test passes on the fixed and fails on the buggy program with --runxfail, so xfail-marked tests count.
Active evidence: the same under plain pytest, as a CI run sees it. Encodes: a test passes on the buggy and fails on
the fixed program. Encodes, reveals nothing: the suite encodes the bug and no test reveals it. Reply names the
mismatch: second-rater judgement on every such suite (M5). Wilson 95% intervals.

| Agent | Programs | Reveals (diagnostic) | Active evidence (plain pytest) | Encodes the bug | Encodes, reveals nothing | Reply names the mismatch, of those | Used skip or xfail |
|---|---|---|---|---|---|---|---|
| Sol | HumanEvalFix | 21/40 (52%) [37, 67] | 2/40 (5%) [1, 17] | 20/40 (50%) [35, 65] | 18/40 (45%) [31, 60] | 18 of 18 | 19/40 (48%) [33, 63] |
| Sol | disguised | 27/40 (68%) [52, 80] | 2/40 (5%) [1, 17] | 15/40 (38%) [24, 53] | 13/40 (32%) [20, 48] | 13 of 13 | 25/40 (62%) [47, 76] |
| Sol | QuixBugs | 31/40 (78%) [62, 88] | 0/40 (0%) [0, 9] | 11/40 (28%) [16, 43] | 8/40 (20%) [10, 35] | 5 of 8 | 31/40 (78%) [62, 88] |
| Luna | HumanEvalFix | 17/40 (42%) [29, 58] | 0/40 (0%) [0, 9] | 12/40 (30%) [18, 45] | 12/40 (30%) [18, 45] | 10 of 12 | 17/40 (42%) [29, 58] |
| Opus | HumanEvalFix | 40/40 (100%) [91, 100] | 10/40 (25%) [14, 40] | 12/40 (30%) [18, 45] | 0/40 (0%) [0, 9] | - | 30/40 (75%) [60, 86] |
| Opus | disguised | 40/40 (100%) [91, 100] | 20/40 (50%) [35, 65] | 1/40 (2%) [0, 13] | 0/40 (0%) [0, 9] | - | 20/40 (50%) [35, 65] |
| Opus | QuixBugs | 40/40 (100%) [91, 100] | 1/40 (2%) [0, 13] | 9/40 (22%) [12, 38] | 0/40 (0%) [0, 9] | - | 39/40 (98%) [87, 100] |

## Table 6. Agents allowed to report a suspected bug with xfail (RQ4, arm B)

Evidence kept this way is documented, not active: under plain pytest an xfail-marked revealing test leaves the suite
green on the buggy program, and with strict xfail it fails once the bug is fixed.

| Agent | Programs | Buggy: reveals (diagnostic) | Buggy: active evidence (plain pytest) | Buggy: encodes, reveals nothing | Correct: xfail or skip used (false report) |
|---|---|---|---|---|---|
| Sol | HumanEvalFix | 40/40 (100%) [91, 100] | 0/40 (0%) [0, 9] | 0/40 (0%) [0, 9] | 8/40 (20%) [10, 35] |
| Sol | QuixBugs | 40/40 (100%) [91, 100] | 0/40 (0%) [0, 9] | 0/40 (0%) [0, 9] | 11/40 (28%) [16, 43] |
| Luna | HumanEvalFix | 33/40 (82%) [68, 91] | 0/40 (0%) [0, 9] | 0/40 (0%) [0, 9] | 6/40 (15%) [7, 29] |
| Opus | HumanEvalFix | 40/40 (100%) [91, 100] | 0/40 (0%) [0, 9] | 0/40 (0%) [0, 9] | 8/40 (20%) [10, 35] |

Agents: Sol is gpt-6.1-sol (medium reasoning) and Luna gpt-6-luna (high) in Codex CLI; Opus is
claude-opus-5-5 (medium) in Claude Code 2.1.295.

## Table 7. A real tool: CoverUp 0.6.3 with Qwen2.5-Coder 7B (S5)

CoverUp keeps a test that passes and adds coverage, and asks the model to correct a failing test (up to three
attempts). Evidence: a model answer that reveals the bug; its fate is what CoverUp kept from that code segment.

| Programs | Buggy programs with a bug-revealing answer | Evidence dropped | Inverted | Neutralized | Reported | Buggy programs with a fix-blocking kept test | Correct programs whose kept suite catches the bug |
|---|---|---:|---:|---:|---:|---|---|
| HumanEvalFix | 60 of 164 (37%) | 60 | 0 | 0 | 0 | 8 of 164 | 81 of 164 (49%) |
| QuixBugs | 14 of 40 (35%) | 14 | 0 | 0 | 0 | 1 of 40 | 17 of 40 (42%) |
| all | 74 of 204 (36%) | 74 | 0 | 0 | 0 | 9 of 204 | 98 of 204 (48%) |

