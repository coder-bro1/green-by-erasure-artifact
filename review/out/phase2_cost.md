# Phase 2 cost and provenance

Computed by `analysis/phase2_cost.py` from each run's manifest.json and llm_calls.jsonl.
Wall clock is manifest start to end (resumed runs include their pauses).

| Run | Model | Digest (first 12) | Harness commit | Calls | Generation | Repair (all) | Judge | Input tokens | Output tokens | Wall clock (h) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| phase2_qwen25_code | qwen2.5-coder:7b-instruct | dae161e27b0e | 811f1a6 | 8,039 | 410 | 4,541 | 3,088 | 3,859,556 | 1,481,709 | 15.0 |
| phase2_qwen35_code | qwen3.5:9b | 56671c2ab938 | 811f1a6 | 6,814 | 424 | 3,510 | 2,880 | 3,549,917 | 1,883,579 | 19.3 |
| phase2_gemma4_code | gemma4:12b | 6114515d63c1 | 7c8b9b3 | 5,799 | 411 | 3,034 | 2,354 | 2,880,445 | 2,059,295 | 18.6 |
| phase2_qwen25_spec | qwen2.5-coder:7b-instruct | dae161e27b0e | a4a0b74 | 8,215 | 412 | 4,671 | 3,132 | 3,911,106 | 1,571,297 | 19.8 |
| phase2_qwen25_seed1 | qwen2.5-coder:7b-instruct | dae161e27b0e | 25e3b2c | 1,578 | 81 | 933 | 564 | 697,502 | 402,323 | 2.5 |
| phase2_qwen25_seed2 | qwen2.5-coder:7b-instruct | dae161e27b0e | 4f541c2 | 1,480 | 80 | 810 | 590 | 657,389 | 230,460 | 2.5 |
| phase2_qwen25_seed3 | qwen2.5-coder:7b-instruct | dae161e27b0e | a36e907 | 1,378 | 80 | 752 | 546 | 605,986 | 206,682 | 2.4 |
| phase2_qwen25_disguised | qwen2.5-coder:7b-instruct | dae161e27b0e | 105b37f | 1,535 | 80 | 851 | 604 | 588,693 | 259,532 | 2.5 |
| phase2_qwen35_disguised | qwen3.5:9b | 56671c2ab938 | 105b37f | 1,125 | 83 | 572 | 470 | 468,990 | 230,207 | 8.1 |
| phase2_gemma4_disguised | gemma4:12b | 6114515d63c1 | 105b37f | 953 | 80 | 481 | 392 | 381,525 | 290,746 | 2.7 |
| phase2_qwen25_natural | qwen2.5-coder:7b-instruct | dae161e27b0e | 2b7992b | 380 | 51 | 197 | 132 | 201,813 | 108,271 | 1.2 |
| phase2_qwen35_natural | qwen3.5:9b | 56671c2ab938 | 12223bf | 447 | 50 | 251 | 146 | 279,083 | 182,174 | 1.9 |
| phase2_gemma4_natural | gemma4:12b | 6114515d63c1 | f4f64e0 | 256 | 51 | 117 | 88 | 124,178 | 122,701 | 1.5 |

Total over the 13 runs: 37,999 calls, 18,206,183 input and 9,028,976 output tokens.

Calls by purpose, all runs: free_repair 19,360, judge 7,493, judge_with_code 7,493, generate 2,293, overwrite_fallback 937, fix_broken 423.
S4 judge replay: 8,322 calls.
S2 generation: 2,460 calls.
Ollama versions recorded: 0.40.1.
