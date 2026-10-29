# C2 step 3: later history of the expected values changed by merged agent pull requests

Computed by `analysis/c2_step3.py` through the GitHub API. RESTORED: a later commit on the default branch put
the original line back in place of the agent's line. CHANGED_AGAIN: a later commit replaced the agent's line
with something else. Counts of changed asserts; pull requests in brackets.

| Agent | Changed asserts (PRs) | Restored | Changed again | Untouched | Agent line at head | Old line at head |
|---|---|---|---|---|---|---|
| OpenAI_Codex | 202 (107) | 6 (5) | 58 (33) | 138 (73) | 91 (54) | 34 (17) |
| Copilot | 186 (62) | 13 (1) | 21 (8) | 152 (56) | 115 (45) | 71 (28) |
| Claude_Code | 178 (20) | 2 (1) | 33 (9) | 143 (16) | 121 (16) | 62 (12) |
| Cursor | 53 (9) | 0 (0) | 6 (2) | 47 (7) | 4 (1) | 6 (1) |
| Devin | 25 (8) | 0 (0) | 0 (0) | 25 (8) | 2 (1) | 2 (1) |
| Google_Jules | 5 (2) | 0 (0) | 0 (0) | 5 (2) | 4 (1) | 2 (1) |
| all | 649 (208) | 21 (7) | 118 (52) | 510 (162) | 337 (118) | 177 (60) |
