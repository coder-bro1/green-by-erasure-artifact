# Green by Erasure: Replication Package

This repository is the replication package for the paper *Green by Erasure: How Failure-Handling Policies Turn
Bug-Revealing Tests into Fault-Enforcing Tests*, submitted to ICST 2027. It contains the experimental harness,
every prompt and configuration, the recorded outputs of all runs, and the scripts that compute the numbers,
tables and figures reported in the paper.

## Study overview

When a test written by an LLM-based test generator fails, the generator cannot tell whether the test is wrong or
has found a bug. Many generators rewrite such a test until it passes. The study measures what this does to tests
that reveal a real bug, and how coverage and mutation score respond.

Three open-weight models (Qwen2.5-Coder 7B, Qwen3.5 9B and Gemma 4 12B, run locally with Ollama) write tests for
the buggy and the fixed version of 204 Python functions from HumanEvalFix and QuixBugs. The same generated tests
are then handled by four failure-handling policies: discard, overwrite, free repair and triage. Every final test
is executed on both versions of its program, which identifies the tests that reveal the bug and those that assert
it. Further studies examine an existing test generator (CoverUp), coding agents, pull requests opened by coding
agents (AIDev) and real bugs (BugsInPy).

## Repository layout

| Path | Contents |
|---|---|
| `src/gbe/` | The harness: test generation, the four policies (`policies.py`), paired execution and labelling (`evaluate.py`), the isolated test runner (`execute.py`), benchmark loaders and the real-bug backend (`c1.py`) |
| `prompts/` | Every prompt sent to a model |
| `configs/` | Run definitions (`runs.json`), model digests and the Ollama version (`models.json`), benchmark pins and sanity evidence, the real-bug tasks |
| `runs/` | Recorded outputs of every run (see below) |
| `analysis/` | Scripts that compute the results in `review/out/`, the figures and the LaTeX number macros |
| `review/out/` | Analysis outputs from which every number in the paper is taken |
| `review/` | Independent consistency and prompt-leakage checks; `review/c2_labels/` holds the pull-request labels of both raters |
| `scripts/` | Run launchers, the coding-agent and CoverUp drivers, and model setup |
| `docs/` | The study specification (`PHASE2_SPEC.md`), the real-bug protocol (`C1_PROTOCOL.md`) and the policy census with its sources (`POLICY_CENSUS.md`) |
| `data/` | The pinned HumanEvalPack rows and QuixBugs sources, benchmark sanity evidence, and the real-bug tasks |
| `figures/` | TikZ sources of the figures |
| `tests/` | Tests of the harness |

Each run folder holds `manifest.json` (model digest, options, harness hashes, timing), `pairs.json`, `tests.csv`
(one row per test and policy, with the outcome on both versions, the label, the fate of each bug-revealing test
and the judge verdicts), `tests_rechecked.csv` (the same after re-executing time-outs with a 30-second limit) and
`summary.csv`. The kill matrices of the mutation analysis are in `runs/phase2_mutation/results/`.

## Mapping from the paper to the package

| Paper | Runs (`runs/`) | Scripts | Outputs (`review/out/`) |
|---|---|---|---|
| Table I, policy census | | | `docs/POLICY_CENSUS.md` |
| RQ1 and RQ2 (Tables II and III, Figs. 2 and 3) | `phase2_qwen25_code`, `phase2_qwen35_code`, `phase2_gemma4_code`, `phase2_mutation` | `analysis/final_numbers.py`, `summary_tables.py`, `kill_power.py`, `figures.py` | `final_numbers.md`, `summary_tables.md`, `kill_power.md` |
| Overwrite without its copy rules (RQ1, RQ2) | `s6_model_only_gemma4`, `s6_model_only_qwen25` | `scripts/s6_model_only_overwrite.py`, `analysis/mutation_extra.py`, `analysis/s6_summary.py` | `s6_model_only.md` |
| Robustness: docstring-only input, disguised pairs, natural faults, sampling at temperature 0.8 | `phase2_qwen25_spec`, `phase2_*_disguised`, `phase2_*_natural`, `phase2_qwen25_seed1` to `seed3` | `analysis/final_numbers.py` | `final_numbers.md` |
| RQ3 (Fig. 4, judge variants, cost analysis) | the three main runs, `s4_judge_specs` | `scripts/s4_judge_specs.py`, `analysis/rq3_metrics.py` | `rq3_metrics.md`, `final_numbers.md` |
| Edit classifier and its validation | the three main runs | `src/gbe/evaluate.py`, `analysis/m5_sample.py`, `m5_agreement.py` | `m5_agreement.md` |
| Section VII-A, CoverUp | `s5_coverup`, `s5_sensitivity` | `scripts/s5_coverup.py`, `analysis/s5_summary.py` | `s5_coverup.md`, `s5_sensitivity.md` |
| Section VII-B, coding agents (Table IV) | `d11` | `scripts/d11.py`, `d11_subagent.py`, `d11_evaluate.py`, `d11_summary.py`, `analysis/d11_plain.py` | `d11_summary.md`, `d11_plain.md` |
| Section VII-C, agent pull requests | `c2`, `review/c2_labels/` | `analysis/c2_*.py` | `c2_*.md` |
| Section VII-D, real bugs | `c1`, `c1_qwen25_code_r2`, `c1_qwen35_code`, `c1_devtests_qwen25_r2` | `analysis/c1_*.py` | `c1_*.md` |

`analysis/make_numbers.py` reads these outputs and writes every number stated in the paper as a LaTeX macro,
together with a table that gives the source of each value.

## Requirements

- Python 3.12 and the packages in `requirements.txt` and `requirements-analysis.txt`.
- To rerun the experiments: Ollama 0.40.1 with the model digests listed in `configs/models.json`, and a GPU with
  at least 12 GB of memory. The experiments were run on Windows 10.
- The figures are compiled with Tectonic; set `GBE_TECTONIC` to its executable before running
  `analysis/figures.py`.

## Reproducing the reported numbers

The recorded runs are sufficient; no model is needed. On Windows:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt -r requirements-analysis.txt
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m pytest -q
.venv\Scripts\python analysis\final_numbers.py
.venv\Scripts\python analysis\summary_tables.py
.venv\Scripts\python analysis\c1_results.py
.venv\Scripts\python analysis\make_numbers.py
```

On Linux or macOS, use `.venv/bin/python` instead. `make_numbers.py` writes `paper/numbers.tex` and
`paper/numbers_sources.md`.

The mutation analysis (`analysis/mutation_run.py`) takes about a day and needs the per-unit working folders, which
are not included (see below). Its results are included in `runs/phase2_mutation/results/`, and the outputs that
depend on it (`kill_power.md`, `rq3_metrics.md`, `s6_model_only.md`) are included in `review/out/`.

## Rerunning the experiments

All runs can be resumed after an interruption. The study runner (`gbe.runner`) also refuses to resume when the
harness files, prompts, model digests or Ollama version have changed.

- **Main study and robustness runs.** `python -m gbe.runner --run-id <id>`, with the run identifiers defined in
  `configs/runs.json`. `scripts/queue_phase2.ps1` runs a list of identifiers in a separate window, and
  `scripts/start_ollama_server.ps1` starts the pinned Ollama server. Time-outs are rechecked with
  `analysis/timeout_recheck.py <run ids>`.
- **Overwrite without its copy rules.** `scripts/s6_model_only_overwrite.py --source phase2_gemma4_code` (and
  `phase2_qwen25_code`) reuses the generated tests of the source run. `analysis/mutation_extra.py` then scores the
  new tests against the recorded mutants, re-applying each mutant and checking it against its recorded hash.
- **Natural faults and judge variants.** `scripts/run_s2.ps1` and `scripts/run_s4.ps1`.
- **CoverUp.** `scripts/run_s5.ps1`, in an environment built from `requirements-coverup.txt` with the two patches
  in `patches/`.
- **Coding agents.** `scripts/queue_d11.ps1`. This requires the vendors' command-line tools and accounts; the
  recorded sessions are in `runs/d11/`.
- **Agent pull requests.** `scripts/c2_download.py` downloads the AIDev tables (1.57 GB, hash-checked), followed by
  `analysis/c2_mine.py`, `c2_step2.py`, `c2_step3.py`, `c2_agreement.py` and `c2_final.py`, in an environment
  built from `requirements-c2.txt`.
- **Real bugs.** Follow `docs/C1_PROTOCOL.md`: `analysis/c1_select.py`, `analysis/c1_install.py`,
  `analysis/c1_build_tasks.py`, then `scripts/run_c1_pipeline.ps1 -RunId c1_qwen25_code_r2`.

## Omitted data and anonymisation

- Per-unit working folders, model response caches and model call logs are omitted for size. They are recreated
  by rerunning the corresponding run.
- BugsInPy and the AIDev tables are not redistributed; the scripts above download them.
- Local file paths are replaced by placeholders such as `<repo>`, `<work>` and `<home>`. E-mail addresses that
  appear in mined pull-request data are replaced by `<email>`.
- The QuixBugs sources in `data/raw/quixbugs_src/` are included at the pinned commit under their MIT licence.
