# C2 step 4: final labels

Computed by `analysis/c2_final.py`. 76 of the 100 sampled agent pull requests whose own commits change an existing expected value together
with code (stratified sample of the 287 candidates after the authorship filter of 19 October, AIDev-pop, Python). Final label: agreed by both raters in 46 cases, adjudicated in 30. Brackets: Wilson 95% intervals
on the sample; the last column weights the agent strata back to all candidates.

| Final WHY | Cases | Share of the sample | Weighted to all candidates |
|---|---:|---|---:|
| I: intended behaviour change | 38 | 50% [39, 61] | 50% |
| W: wrong test repaired | 9 | 12% [6, 21] | 12% |
| E: possible erasure | 6 | 8% [4, 16] | 8% |
| M: no real change (matcher error) | 10 | 13% [7, 23] | 13% |
| U: can't tell | 13 | 17% [10, 27] | 17% |

- The 287 pull requests are matcher candidates. Real expectation changes (not M): 66 of 76 in the sample (87% [77, 93]); weighted to all candidates 87%, about 249 pull requests.

- The description says that an existing expectation changed: 15 of 76 (20% [12, 30]); among the 66 real changes (not M): 14.
- Possible erasures (E): 6; of them merged 4, described as a test change 0.
- Among the real changes the raters could decide (I, W, E): I 38, W 9, E 6 of 53.

| Agent | Cases | I | W | E | M | U | Says so (Y) |
|---|---:|---:|---:|---:|---:|---:|---:|
| OpenAI_Codex | 32 | 16 | 4 | 4 | 4 | 4 | 8 |
| Copilot | 17 | 8 | 2 | 1 | 4 | 2 | 3 |
| Devin | 12 | 7 | 2 | 1 | 0 | 2 | 2 |
| Claude_Code | 10 | 3 | 1 | 0 | 1 | 5 | 0 |
| Cursor | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| Google_Jules | 2 | 1 | 0 | 0 | 1 | 0 | 2 |

Adjudication of the differing cases: final WHY equal to rater A 14, to rater B 23, to neither 2 (of 30; equal to both where only SAYS differed).

Cases with final label E:

- C016 (OpenAI_Codex, merged): Enable Chalice multipart uploads (https://github.com/graphql-python/graphql-server/pull/134)
- C017 (OpenAI_Codex, not merged): Implement HTML file browser for preset tools (https://github.com/charlesvestal/extending-move/pull/38)
- C030 (Copilot, merged): Fix inferred parameters missing from dataset when explicitly added (https://github.com/microsoft/Qcodes/pull/7240)
- C055 (OpenAI_Codex, merged): [alpha_factory] add module entry for business v3 demo (https://github.com/MontrealAI/AGI-Alpha-Agent-v0/pull/2053)
- C067 (OpenAI_Codex, merged): feat: add tool estimation config and rate limiting infrastructure (https://github.com/wshobson/maverick-mcp/pull/24)
- C086 (Devin, not merged): feat: implement hierarchical agent delegation with allowed_agents parameter (https://github.com/crewAIInc/crewAI/pull/2070)
