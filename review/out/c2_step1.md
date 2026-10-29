# C2 step 1: expected-value changes in agent pull requests (AIDev-pop, Python)

Computed by `analysis/c2_mine.py`. A pull request counts when it changes a test file and another Python
file. Expected-value change: a one-line assert whose checked side is unchanged and whose other side changed.

Python pull requests in AIDev-pop: 13,256 (merged 9,442); diff rows read: 1,775,765; Python file diffs skipped: 51,009 (from 2,206 merge commits, 5,424 commits not by the agent and 3,928 commits that belong to an earlier pull request).

| Agent | Python PRs | Touch tests and code | With an expected-value change | Merged, of those | Test edit in a later commit than the code | Expected-value changes | PRs adding skip or xfail |
|---|---:|---:|---:|---:|---:|---:|---:|
| OpenAI_Codex | 7,971 | 1,746 | 116 (7%) | 91 | 8 | 253 | 84 |
| Copilot | 2,695 | 836 | 79 (9%) | 59 | 12 | 271 | 57 |
| Devin | 1,346 | 494 | 40 (8%) | 7 | 7 | 103 | 30 |
| Cursor | 790 | 182 | 13 (7%) | 8 | 3 | 64 | 4 |
| Claude_Code | 402 | 180 | 37 (21%) | 20 | 6 | 293 | 31 |
| Google_Jules | 52 | 19 | 2 (11%) | 2 | 0 | 5 | 3 |
| all | 13,256 | 3,457 | 287 (8%) | 187 | 36 | 989 | 209 |

Test-file patches missing from AIDev (too large for the GitHub API): 470.
