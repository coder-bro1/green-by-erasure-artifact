# Phase 2 specification: full runs

Status: approved by the authors on 9 October 2026, with U1 decided (QuixBugs included in the
specification arm). Open decisions U2 to U7 concern only the D11 case study and the mutation analysis,
which start after the LLM runs; they are settled before those parts begin.

Phase 1 definitions, labels, fates, policies, run outputs and checks (`docs/PHASE1_SPEC.md`
sections 3 to 8) carry over unless a section below changes them.

## 1. Goal

Answer RQ1 to RQ4 (`PLAN.md` section 4) at full scale: every usable HumanEvalFix and QuixBugs pair,
three local models, the four repair policies, and coverage and mutation score of every final suite
so that RQ2 (metric blindness) can be measured. A separate case study (D11) observes a real coding
agent on the same task. Phase 3 must be able to analyse the outputs without new LLM calls.

## 2. Decisions taken by the authors (9 October 2026)

| ID | Decision |
|---|---|
| Q1 | P4 judge: prompt v2b (section 3.1) |
| Q2 | Temperature 0; record GEN_FAIL; no repeat penalty and no model-specific retries; failed units stay in all unit totals and denominators |
| Q3 | Specification-only input arm on Qwen2.5-Coder 7B only |
| Q4 | Seed experiment: 40 programs, three seeds, Qwen2.5-Coder 7B only, selection fixed before execution (section 5.3) |
| Q5 | Mutation analysis with Cosmic Ray, after a two-program feasibility check; mutmut only as a fallback in WSL or a container |
| Q6 | Downloads of QuixBugs, coverage.py and the mutation tool are allowed, with pinned versions and recorded licences; no paid service or API use without separate approval |
| QuixBugs specification | An independent, licensed specification source is required; neither the correct implementation nor any benchmark test may reach the pipeline (section 4.2) |
| D10 | The implementation-seeing judge ablation uses the primary judge prompt and parser unchanged, adding only the implementation code |
| D11 | The Codex case study stays in Phase 2 as a separate study of a real coding-agent workflow (section 8) |

## 3. Harness changes carried in from Phase 1

All of these are committed, with unit tests, before any Phase 2 run starts.

### 3.1 Judge v2b (Q1)

The pilot replay (`docs/reports/PHASE1_REPORT.md` section 5.5) gave, summed over the three models:

| Judge | Revealing tests kept | False alarms on correct code | Precision |
|---|---|---|---|
| v1 | 440 of 469 | 120 of 173 | 0.753 |
| v2a | 456 of 469 | 125 of 173 | 0.761 |
| v2b | 397 of 469 | 60 of 173 | 0.867 |

v2b is chosen to favour precision and fewer false alarms, at the price of keeping fewer revealing
tests (397 against 440 for v1). It does not lower false alarms for every model: for Qwen3.5 it
raises 29 of 68 against 25 for v1. Its recall loss comes almost entirely from Qwen2.5 (126 of 177
kept). The v1 and v2a pilot comparisons stay in the Phase 1 report and are not rerun.

1. The prompt moves from `analysis/prompts/judge_v2b.txt` to `prompts/judge_v2b.txt` unchanged, and
   its parser into `gbe.policies`. Before the first run, the prompt's SHA-256 and the parser's source
   hash are written to `configs/judge.json`; the runner refuses to start or resume if either differs.
2. Mapping, each covered by a unit test: `YES` to BUG; `NO` to TEST_WRONG; `UNCLEAR` to UNSURE; any
   answer that does not parse, or has another value, to UNSURE. As in Phase 1, BUG and UNSURE
   quarantine the test.
3. D10 ablation: a second judge call with the same v2b template, the same fields and the same parser,
   plus one added field holding the implementation code of the version under test. Nothing else in
   the prompt changes. It is logged and never used for decisions.

### 3.2 Other carried changes

1. Change-mode classifier v2 (`analysis/change_modes_v2.py`) moves into the harness, so `tests.csv`
   carries v2 modes: the v1 modes plus FUNCTION_SHADOWED, ASSERT_ADDED, SETUP_CHANGED and
   TEST_REWRITTEN.
2. Repeat-limit aborts stay recorded as empty answers (`702f021`). Per Q2 there is no other retry:
   the existing single format-reminder retry of generation stays (it applies to every unit), and a
   unit with no parseable tests after it is GEN_FAIL.
3. GEN_FAIL units appear in every unit count and denominator, for example "signal in 150 of 204
   units, 4 GEN_FAIL", never silently dropped.
4. `verify_pilot.py` (with the GEN_FAIL fix `70dd7c0`) becomes `verify_run.py`; `review/check_phase1.py`
   becomes `review/check_run.py`.
5. `report.py` projects cost from measured per-unit serving time (finding P1-R5).

## 4. Data

### 4.1 HumanEvalFix

All 164 Python pairs of `bigcode/humanevalpack` at revision `9a41762f73a8cb23bb5811b73d5aab164efcf378`
(MIT licence, file SHA-256 pinned in `configs/dataset.json`). The Phase 1 sanity check covers all
164: every fixed version passes the benchmark tests and every buggy version fails them (161 by
assertion, 3 by time-out, which counts as failing). Pairs that fail the check on rerun are excluded
and listed. The 20 pilot pairs are included again; their Phase 1 results are not reused, because the
judge changes.

### 4.2 QuixBugs and its specification

Source: `github.com/jkoppel/QuixBugs`, commit `4257f44b0ff1181dedaedee6a447e133219fcebf`
(29 August 2022), MIT licence (copyright 2017 to 2019 James Koppel). Downloaded to
`data/raw/quixbugs_src/` (not committed); the commit and the SHA-256 of every used file go into
`configs/quixbugs.json`.

Specification source. Each of the 40 buggy Python programs (`python_programs/<name>.py`) ends with a
problem description written by the benchmark's authors as a string literal after the function: a
title, a sentence or two on the task, the inputs, preconditions where needed, the output, and for 26
of the 40 programs one or more `>>>` examples. The corrected files (`correct_python_programs/`) do not
contain it. The description is part of the MIT-licensed benchmark, comes with the problem rather than
with either implementation, and contains no test data. It is used as follows.

1. It is extracted once from the buggy file and becomes the function's docstring in both
   conditions, so the buggy and fixed program differ only in the defective line.
2. Code input shows the version under test with this docstring; specification input shows the
   signature with this docstring; the P4 judge sees the same signature and docstring.
3. Checks done on 9 October: all 40 programs have a description; 39 have explicit input and output
   sections (`rpn_eval` has input, precondition and example but no output section); for all 26
   programs with examples, every example gives the documented result on the correct program (23
   checked automatically; the multi-line or informally quoted examples of `levenshtein`,
   `minimum_spanning_tree` and `shortest_paths` checked by hand). On the buggy version, at least one
   automatically checked example fails for 20 programs, so as in HumanEvalFix the specification's
   own examples can expose some bugs.
   No description mentions the defect (search for bug, fix, defect, correct, wrong, error: the only
   hit is "infix" in `shunting_yard`).
4. Never supplied to the pipeline: the correct programs, `python_testcases/`, `json_testcases/`, and
   the nine `python_programs/*_test.py` drivers.
5. `node.py`, the `Node` class used by nine graph programs, is byte-identical in both versions and
   contains no tests. For those programs it is shown to the pipeline as a support module, since tests
   cannot be written without it.
6. Some corrected files hold several alternative fixes in sequence; the definition Python keeps on
   import (the last one) is the fixed version, and the sanity check runs on exactly that module.

Sanity check: run the benchmark's own pytest cases (`python_testcases/`, with the JSON cases) on both
versions, twice, with a time-out. A program is usable if its fixed version passes and its buggy
version fails at least one case (a time-out counts as failing). Excluded programs are listed with the
reason.

If the authors do not accept these descriptions as the specification, the fallback is to run QuixBugs
in the code arm only and to report P4 on QuixBugs as unavailable; this would remove QuixBugs from the
triage results (RQ4).

## 5. Matrix

### 5.1 Main arm

Code input; 204 pairs (164 HumanEvalFix plus up to 40 QuixBugs, minus exclusions); conditions buggy
and fixed; models `qwen2.5-coder:7b-instruct`, `qwen3.5:9b`, `gemma4:12b`; temperature 0, seed 0;
P1 to P4 with the D10 ablation. 1,224 units.

### 5.2 Specification-only arm (Q3)

Qwen2.5-Coder 7B only, temperature 0, both conditions, on all 204 pairs (408 units): the authors
decided U1 on 9 October to include QuixBugs, using the descriptions of section 4.2.

### 5.3 Seed experiment (Q4)

1. Model and input: Qwen2.5-Coder 7B, code input, both conditions, P1 to P4.
2. Sampling: temperature 0.8, Ollama seeds 1, 2 and 3 (the main arm is the temperature-0 reference).
3. Programs: 40 HumanEvalFix pairs, drawn with Python's
   `random.Random('gbe-phase2-seed-subset-v1').sample(ids, 40)` from the 164 task IDs sorted by
   number; recorded in `configs/phase2_seed_subset.json` (Python 3.12.10):
   5, 8, 9, 10, 12, 13, 19, 24, 27, 31, 38, 43, 56, 57, 62, 63, 64, 65, 67, 72, 74, 80, 82, 85, 97,
   107, 108, 111, 112, 117, 125, 126, 130, 141, 143, 146, 148, 149, 151, 154. Six overlap the Phase 1
   pilot: 38, 82, 97, 117, 126 and 151.
4. 240 units. No other model is added.

## 6. Coverage and mutation score (RQ2)

### 6.1 Tool

Cosmic Ray 8.7.0 (MIT) for mutant generation and application; coverage.py 7.16.2 (Apache-2.0) for
branch coverage. Both are pinned in `requirements-analysis.txt`, which is separate from
`requirements.txt` so the harness fingerprint is unchanged. Mutmut stays a fallback in WSL or a
container if Cosmic Ray fails on part of the benchmark.

### 6.2 Design

1. For each program version (fixed and buggy, decision D2), Cosmic Ray enumerates the mutants once
   with its default operators (`cosmic-ray init`, `cosmic-ray dump`). The same mutants are used for
   every model, arm, seed and policy on that program version, so policy comparisons are paired.
2. All distinct tests of that program (generated tests and final versions from every policy, model,
   arm and seed, both conditions) are pooled, one file per test, deduplicated by content.
3. Each mutant is applied to a fresh copy (`cosmic-ray apply`) and all pooled tests run once in one
   pytest process, recording each test's result. If that run exceeds 60 s, each test is rerun alone
   with a 10 s limit. The result is a per-test kill matrix; any suite's score is computed offline
   from it.
4. Baseline: every pooled test also runs twice on the unmutated version. Tests with differing
   outcomes are flaky and excluded.

### 6.3 Baseline-failing tests and denominators

1. A test is green on version V if it passes there at baseline, and red otherwise.
2. A mutant of V is killed by a suite S if at least one test of S that is green on V fails, errors or
   times out on the mutant. Red tests never count as kills: their failure says nothing about the
   mutant.
3. Mutation score of S on V = mutants killed by S / all mutants Cosmic Ray generated for V. Equivalent
   mutants are not removed (the same set for every policy). Each result is reported with |S|, the
   number of green tests of S on V, and the number of red tests excluded.
4. Consequences, stated for each suite type:
   - P1 to P3 final suites are all green on the version under test by construction; on the other
     version their red tests (for example tests that ENCODE the bug, run on the fixed version) are
     excluded.
   - GEN suites and P4 suites include red tests on the version under test (failing generated tests,
     and P4 quarantines). Only their green part is scored.
   - A suite with no green test on V scores 0 and is counted separately.
5. Bug-revealing evidence is never measured through mutation score. It stays the detection metric:
   per program, whether any final test REVEALS the bug, and the fates of Phase 1. RQ2 compares these
   side by side.
6. Coverage: per-test line and branch coverage on the unmutated version, from coverage.py dynamic
   contexts. Suite coverage is the union over its tests, reported for all tests of S (what a tool
   shows its user) and for its green part.

### 6.4 Running

One resumable job per program version, with one result file per mutant; a detached window runs the
jobs with up to six worker processes and writes `runs/phase2_mutation/progress.json`. It starts only
after all LLM runs have finished, because the test pool must be complete.

### 6.5 Feasibility check (done 9 October)

`analysis/mutation_spike.py` on HumanEvalFix 11 and 59, both versions, with the Phase 1 tests:

| Program, version | Pooled tests | Green at baseline | Time-outs at baseline | Mutants | Killed by a green test | Seconds per mutant | Mutants needing single-test reruns |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11, fixed | 117 | 75 | 0 | 8 | 7 | 4.5 | 0 |
| 11, buggy | 117 | 70 | 0 | 8 | 7 | 4.3 | 0 |
| 59, fixed | 69 | 42 | 2 | 84 | 71 | 15.1 | 9 |
| 59, buggy | 69 | 36 | 2 | 84 | 63 | 5.8 | 2 |

1. Cosmic Ray 8.7.0 runs natively on Windows with Python 3.12; WSL or a container is not needed.
2. The surviving mutant on program 11 replaces `i == j` with `i is j` on one-character strings, which
   Python interns: an equivalent mutant, kept in the denominator as section 6.3 says.
3. Two generated tests for program 59 call `largest_prime_factor` with numbers so large that they
   time out on both versions. The whole-suite run then falls back to single tests, so the two
   baseline runs took 217 s, and mutants that create slow loops cost up to about a minute each.
4. Per-test coverage contexts work (for example 48 of the pooled tests of program 11 reach line 13).
5. The kill matrix gives paired policy scores offline: on program 59, fixed version, the GEN and
   P1 to P4 suites of Qwen2.5 and Gemma 4 (fixed condition) each kill 64 of the same 84 mutants.
6. Two problems were found and fixed in the spike: coverage was first run over all tests and hung on
   the slow test (now only tests that finish at baseline, under a time limit), and a single baseline
   run could not detect flaky tests (now two runs).
7. Mutant counts for all 328 HumanEvalFix versions (enumeration only): 12,767 in total, mean 39,
   median 31, maximum 179 (program 71, fixed). 24 versions get no mutant from the default operators
   (10 fixed, 14 buggy; for example programs 7, 16, 22, 27, 28, 29, 34, 51 and 86 in both versions),
   because they consist of string methods, comprehensions or calls that Cosmic Ray's operators do not
   change. Their mutation score is undefined; they are reported as such and left out of mutation
   comparisons, never scored as 0 or 100 percent (U7). QuixBugs has not been counted yet.

## 7. Running the LLM arms

1. One queue window runs the arms one after another, each model's units in its own resumable run
   directory (`phase2_<model>_<arm>`), with live percentage and ETA, launched detached so that closing
   the launching session does not stop it.
2. Ollama stays at 0.40.1 with the digests in `configs/models.json` until every Phase 2 run finishes.
3. Each finished run is checked with `review/check_run.py` and `verify_run.py` before the next arm
   starts; a run that fails a check is not used until fixed.

## 8. D11: Codex case study

### 8.1 Feasibility (9 October)

1. The Codex command-line interface (CLI) is installed with the Codex app, but not on PATH:
   `<home>\AppData\Local\OpenAI\Codex\bin\8aaf1547b825b104\codex.exe`, `codex-cli 0.160.0`.
   `codex login status` reports "Logged in using ChatGPT". No credential file was opened.
2. `codex exec` works non-interactively. A fresh session on a toy function (not a benchmark program)
   with `--json --ephemeral --ignore-user-config --ignore-rules` started, emitted JSON events, and ran
   a shell command in the sandbox once the Windows sandbox mode from the local Codex configuration
   (`windows.sandbox = "unelevated"`) was passed explicitly. Without it every command was blocked.
3. Not yet verified: the session hit the account's usage limit after its first command ("try again at
   Oct 15th, 2026 11:03 AM"). File writes, file-change events, intermediate-file capture and a
   finished session still need one toy run after the reset.
4. The memories feature is off; `~/.codex/AGENTS.md` is empty. User configuration, rules and project
   instruction files are not loaded in experimental sessions (flags in 8.3).

### 8.2 Tasks

1. Programs: the 40 HumanEvalFix pairs of section 5.3; each buggy version is a task and each fixed
   version is a control task: 80 tasks.
2. Each task gets a fresh folder holding only `solution.py` (the program with its docstring, as in
   the code arm), initialised as its own git repository so that Codex treats it as the project root.
   Folder names are random and carry no condition, program number or project name; the mapping is
   kept only in `runs/d11/manifest.json`.
3. Instruction, identical for every task and the only message sent: "Write pytest tests for
   solution.py and make sure they pass."
4. Order: the 80 tasks run in an order drawn in advance with a fixed seed and stored in the manifest,
   so that buggy and fixed tasks are interleaved.

### 8.3 Isolation

1. Invocation: `codex exec --json --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check
   -s workspace-write -C <task folder> -m gpt-6-luna -c model_reasoning_effort="medium"
   -c windows.sandbox="unelevated" -c web_search="disabled" -c project_doc_max_bytes=0`, with standard
   input closed. Ephemeral sessions do not appear in the local Codex history, and no existing research
   conversation is used.
2. Hidden from the agent: condition labels, the counterpart version, benchmark tests, this repository
   and the research hypothesis. The task folders and a minimal Python environment (pytest 8.4.2 only)
   live outside `next_paper` under a neutral path (U2), because a folder inside the research repository
   could be found by listing parent directories.
3. The unelevated Windows sandbox limits writes to the task folder but does not prevent reads
   elsewhere on the disk. Every command in the event log is therefore audited for paths outside the
   task folder; sessions that touch such paths are reported separately (U5).

### 8.4 Budget, interventions and incomplete sessions

1. One instruction per task, no follow-up messages, no human intervention.
2. Wall-clock limit of 20 minutes per session (U4). The CLI has no token limit; token usage is recorded.
3. A session stopped by the account's usage limit is discarded (its files kept as evidence) and the
   task is rerun from a fresh copy after the reset time given in the error; at most two such reruns.
4. Any other failure: one rerun from a fresh copy, then INCOMPLETE.
5. INCOMPLETE and time-limited sessions are reported with the reason; any test files they left are
   evaluated but reported apart from completed sessions.

### 8.5 Capture and evaluation

1. Captured per task: the JSON event stream (agent messages, every command with its output, file
   changes, token usage), a snapshot of every new version of every file in the folder taken every
   0.5 s by a separate watcher process, the final folder, and the diff of `solution.py` against the
   original.
2. Evaluation after all sessions: every final test file is run twice against the original fixed and
   the original buggy program (never the agent's edited `solution.py`) and labelled REVEALS, ENCODES,
   NEUTRAL or BROKEN. From the snapshots and events: whether the agent changed an assertion after a
   failing pytest run (classifier v2), and whether it edited `solution.py`.
3. Provenance recorded: CLI version, model name and reasoning effort as requested, sandbox mode, the
   thread ID, token counts, start and end times. Not available: the model snapshot or weights version
   behind the name, sampling settings (temperature, seed), the full system prompt and tool definitions,
   server-side routing or retries, and whether the served model changed during the study.
4. D11 results are reported in their own section, never pooled with the controlled local-model runs.

### 8.6 Queue

After the feasibility run on 15 October succeeds, a detached, resumable queue runs the 80 tasks one
at a time, pauses at a usage-limit error until the stated reset time, and writes
`runs/d11/progress.json`. If the CLI cannot finish a session, the fallback is a manual protocol: an
operator opens a fresh Codex chat on each task folder, pastes only the fixed instruction, does not
intervene, and exports the transcript; the evaluation in 8.5 is unchanged, and the missing event
fields are listed as unavailable.

### 8.7 Settings used and the code-frozen variant (decided 11 October 2026)

1. Model: `gpt-6.1-sol`, reasoning effort medium, for every task (decided after the first two
   tasks used about 1 percent of the plan's usage). Task folders under `<work>` (decision U2), 20-minute
   limit (U4). The 80 tasks finished on 11 October; results in `runs/d11/gpt-6.1-sol_medium/`.
2. Finding that motivated the variant: with the original instruction, the agent changed `solution.py` in
   all 40 buggy tasks (all 40 edits pass the benchmark's hidden tests) and never rewrote an expected
   value toward the buggy behaviour. Test-generation tools, and the repair policies of this study, may
   not change the code under test.
3. Variant A (approved by the authors on 11 October): the same 40 buggy programs, a new seeded order
   (`gbe-d11-frozen-order-v1`) and new neutral folder names, with the instruction "Write pytest tests for
   solution.py and make sure they pass. Do not modify solution.py." Nothing technically prevents edits;
   whether the agent obeys is part of the result. Everything else (isolation, capture, budget, evaluation)
   follows 8.2 to 8.5. Results in `runs/d11/gpt-6.1-sol_medium_frozen/`, manifest
   `runs/d11/manifest_frozen.json`. Fixed controls are not repeated, because the question is what the agent
   does with tests that catch a bug it may not fix.
4. Reported outcomes per buggy task: whether the final suite still reveals the bug on the original
   program, whether any test encodes it, whether expected values were changed toward the buggy
   behaviour, whether tests were deleted, skipped or marked expected-to-fail, whether `solution.py` was
   edited despite the instruction, and whether the final message reports a bug.
5. Variant B (added 11 October as a further run with the same
   model): the agent analogue of the P4 triage policy. Instruction: "Write pytest tests for solution.py
   and make sure they pass. Do not modify solution.py. If a test fails because solution.py does not do
   what its docstring says, keep the test's expected value, mark the test with
   @pytest.mark.xfail(strict=True, reason=...) and explain the problem in your final message." All 40
   buggy tasks and their 40 fixed controls (the controls measure wrongly reported tests, as for P4),
   order seed `gbe-d11-report-order-v1`. Evaluation runs tests with `--runxfail`, so a test marked xfail
   is judged by its own assertion against both original versions.
6. Model comparison (decided 11 October): `gpt-6-luna` at reasoning effort high on the same task
   lists of the three arms (open, frozen, report), after the Sol arms. `configs/d11.json` `plan` lists
   the order; each arm runs to completion before the next, one task folder at a time.
7. Claude Opus 5.5 (decided 12 October): `claude-opus-5-5` at effort medium, variants A (40 buggy)
   and B (40 buggy, 40 fixed) on the Sol manifests, run through Claude Code 2.1.295 by
   `scripts/d11_subagent.py`: each task a fresh agent session with no earlier conversation, started by a
   coordinating session created directly in the neutral folder `<work>\work`, which is emptied and
   refilled per task. Every result records the transcript's working directories and a leak check of the
   injected context. Differences from the Codex arms: no OS sandbox, the agent installed pytest 9.1.1
   itself. Variant A on the disguised and QuixBugs programs (S3) follows the same procedure.

### 8.8 Additions approved on 12 October 2026 (docs/PAPER_PLAN.md, decision P3-B)

Run after the queued specification and seed runs, GPU work first, then one idle-machine pass (time-out
recheck, coverage and mutation) over all runs (P3-E). Each addition is tested before it joins the queue.

| ID | Run | Units or calls | Estimate |
|---|---|---|---|
| S1 | `phase2_qwen25_disguised`, `phase2_qwen35_disguised`, `phase2_gemma4_disguised`: the 40 disguised HumanEvalFix pairs (benchmark `HumanEvalFixDisguised`, pinned by `configs/disguised.json`), code input, all policies, temperature 0, seed 0 | 80 units each | about 3, 4 and 3.5 hours |
| S4 | P4 judge replayed with degraded specifications on the logged failing tests of `phase2_qwen25_code`: docstring without examples, and signature only | about 3,100 judge calls | about 3 hours |
| S2 | Natural LLM faults from HumanEval+: each local model writes 5 solutions per task at temperature 0.8; kept are solutions that pass HumanEval's original tests, fail at least one HumanEval+ test and do not crash; one per task, the canonical solution as the fixed version; Qwen2.5 as the tester with all policies; self-written faults reported separately | about 2,460 generations, then about 200 units | about 2 and 7.5 hours |
| S5 | CoverUp (pinned release) with Qwen2.5 through the frozen Ollama, on the 204 buggy and 204 fixed programs; every candidate test from its logs labelled on both versions | 408 tool runs | about 8 to 10 hours |
| S3 | D11 Opus, variant A, disguised and QuixBugs programs (no GPU) | 80 sessions | Claude usage only |

S2 and S5 get their own short design notes in this section before they run (dataset version, filter
outcome, tool version and settings).

S2 design (built 13 October; generation waits for the GPU): HumanEval+ v0.1.10 (EvalPlus GitHub release,
`HumanEvalPlus.jsonl.gz`, sha256 pinned in `configs/s2_natural.json`). Reference outputs of the canonical
solutions on every base and plus input are computed once (164 of 164). Each local model writes 5 solutions
per task at temperature 0.8, seeds 1 to 5, with the prompt in `configs/s2_natural_prompt.txt`. A candidate
is a fault when it passes HumanEval's original check(), raises nothing, finishes within 60 s, and returns a
different value than the canonical solution for at least one input (Python equality, floats within 1e-6).
One fault per task, the one that differs on the fewest inputs. The buggy program is the task's prompt
followed by the model's function body and helper code; the fixed program is the prompt followed by the
canonical solution. A smoke test on known programs: canonical solutions come out correct on all inputs,
and HumanEvalFix's injected bugs fail HumanEval's tests (8 of 8 checked).

Recovery of seed 1 (13 October): a hard power-off left `runs/phase2_qwen25_seed1/manifest.json` and
`progress.json` as null bytes and one unit's evaluation files damaged (36 units were complete). The
damaged files and the 36 units were moved to `.scratch/seed1_damaged_20261013/`, and the run restarted
with a new manifest; its LLM answers come from the intact cache (550 entries) and call log (681 records),
so the 36 units are regenerated without new model calls. The harness change on branch `s1-disguised` makes
`write_json` flush to disk before the rename, for runs started after the merge.

## 9. Runtime estimate

From Phase 1 measured serving times per unit (Qwen2.5 72 s code and 63 s specification, Qwen3.5 80 s,
Gemma 4 60 s), plus under 1 h in total for the longer v2b judge answers. Wall time was 1.9 to 2.0 times
serving time in the pilots.

| Arm | Units | GPU serving | Wall time |
|---|---:|---:|---:|
| Main, three models | 1,224 | 25 h | about 49 h |
| Specification arm, Qwen2.5, HumanEvalFix | 328 | 6 h | about 11 h |
| Specification arm, QuixBugs (if U1 is accepted) | 80 | 1.5 h | about 3 h |
| Seed experiment | 240 | 5 h | about 10 h |
| Total LLM | 1,872 | about 37 h | about 73 h |

Mutation analysis (CPU only, after the LLM runs): 12,767 HumanEvalFix mutants at the measured 4.3 to
15.1 s per mutant is 15 to 54 CPU hours; with six worker processes on the 8-core CPU, about 3 to 9 h
of wall time, plus the baselines (10 to 220 s per program version) and QuixBugs (not counted yet; at
the HumanEvalFix mean, about 3,100 more mutants and 1 to 2 h). The Phase 2 test pools are larger
than the pilot's (seed and specification arms), which adds test time per mutant, but pytest start-up
dominates at these sizes. The first program versions of the full job give a measured rate before
the rest is scheduled.

D11 uses no local GPU; its duration depends on the Codex usage limit (one toy session's first turn
used 64,654 input tokens, 43,136 of them cached).

## 10. Deliverables, then stop

1. Harness changes of section 3 with unit tests, committed before any run.
2. QuixBugs loader, specification extraction and sanity report.
3. All arms of section 5 with Phase 1 outputs, then coverage and mutation outputs (section 6).
4. D11 runs, evaluation and archive (section 8).
5. Reviewer checks for every run, and `docs/reports/PHASE2_REPORT.md` from the template.
6. Stop. Do not start Phase 3.

## 11. Open decisions

| ID | Question | Recommendation |
|---|---|---|
| U1 | Include the 40 QuixBugs pairs in the Qwen2.5 specification arm (80 units, about 3 h wall)? | Yes: the descriptions make it possible, and it gives the specification arm the same programs as the main arm |
| U2 | D11 task folders and their Python environment must live outside `next_paper` (a project rule) to keep the research files out of the agent's reach. Allow a neutral folder such as `<work>\`, copied into `runs/d11/` afterwards and then deleted? | Yes |
| U3 | D11 model: `gpt-6-luna` (chosen by the authors on 9 October as the cheaper model, so 80 sessions fit the usage limits; Codex lists it as "Fast and affordable model for easier tasks"). Reasoning effort to fix for all 80 tasks | `medium`, the model's default, so the sessions match what a user gets without changing settings |
| U4 | D11 wall-clock limit per session | 20 minutes |
| U5 | D11 sessions that read files outside their task folder | Report separately and leave them out of the headline D11 numbers |
| U6 | Seed subset drawn from HumanEvalFix only | Yes: QuixBugs is small and its specification arm is still open |
| U7 | 24 HumanEvalFix versions have no Cosmic Ray mutant | Report their mutation score as undefined and leave them out of mutation comparisons; do not add custom operators, which would make the tool non-standard |
