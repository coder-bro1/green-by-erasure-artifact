# C2 step 2: disclosure and review of expected-value changes

Computed by `analysis/c2_step2.py`. Pull requests by agents in Python repositories of AIDev-pop that change
a test file and other code; "with" = at least one expected-value change in an existing assert (step 1).

| Agent | Group | PRs | Mentions tests | Explains a test change | Any human comment | Human review comment on the changed test file | Its diff context shows the changed assert | Anchored on the changed assert | Changes requested | Merged |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OpenAI_Codex | with | 116 | 90 (78%) | 46 (40%) | 25 (22%) | 4 (3%) | 1 (1%) | 0 (0%) | 1 (1%) | 91 (78%) |
| OpenAI_Codex | without | 1,630 | 1,490 (91%) | 350 (21%) | 230 (14%) | - | - | - | 11 (1%) | 1,325 (81%) |
| Copilot | with | 79 | 74 (94%) | 44 (56%) | 74 (94%) | 25 (32%) | 9 (11%) | 3 (4%) | 27 (34%) | 59 (75%) |
| Copilot | without | 757 | 697 (92%) | 220 (29%) | 537 (71%) | - | - | - | 111 (15%) | 391 (52%) |
| Devin | with | 40 | 36 (90%) | 15 (38%) | 34 (85%) | 2 (5%) | 1 (2%) | 0 (0%) | 2 (5%) | 7 (18%) |
| Devin | without | 454 | 402 (89%) | 154 (34%) | 269 (59%) | - | - | - | 17 (4%) | 60 (13%) |
| Cursor | with | 13 | 5 (38%) | 2 (15%) | 8 (62%) | 1 (8%) | 0 (0%) | 0 (0%) | 0 (0%) | 8 (62%) |
| Cursor | without | 169 | 88 (52%) | 30 (18%) | 82 (49%) | - | - | - | 2 (1%) | 67 (40%) |
| Claude_Code | with | 37 | 37 (100%) | 17 (46%) | 26 (70%) | 2 (5%) | 0 (0%) | 0 (0%) | 1 (3%) | 20 (54%) |
| Claude_Code | without | 143 | 124 (87%) | 42 (29%) | 83 (58%) | - | - | - | 7 (5%) | 90 (63%) |
| Google_Jules | with | 2 | 2 (100%) | 1 (50%) | 1 (50%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 2 (100%) |
| Google_Jules | without | 17 | 7 (41%) | 3 (18%) | 7 (41%) | - | - | - | 0 (0%) | 6 (35%) |
| all | with | 287 | 244 (85%) | 125 (44%) | 168 (59%) | 34 (12%) | 11 (4%) | 3 (1%) | 31 (11%) | 187 (65%) |
| all | without | 3,170 | 2,808 (89%) | 799 (25%) | 1,208 (38%) | - | - | - | 148 (5%) | 1,939 (61%) |
