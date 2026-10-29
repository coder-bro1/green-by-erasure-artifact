# C1 protocol: replication on real repository bugs (stage C)

Status: fixed on 19 October 2026, before any download or run (decision P3-J, docs/PHASE2_REVISION_PLAN.md
section 4, stage C). Changes after this date are recorded in section 9 with the reason, never silently.

## 1. Question

Does the controlled result (RQ1 fault enforcement and RQ3 price of preservation) hold for developer-fixed bugs
in real Python projects, beyond benchmark functions? The same policies (P1 discard, P2 overwrite, P3 free
repair, P4 triage) process the same generated tests; only the subjects change.

## 2. Source

BugsInPy (Widyasari et al., ESEC/FSE 2020 demo), the GitHub repository soarsmu/BugsInPy at a commit recorded at
download time: 501 bugs from 17 Python projects, each with buggy and fixed commit, the developer's fix patch and
the developer's bug-revealing test command.

## 3. Eligibility, checked in this order (attrition reported at every step)

1. The fix changes the body of exactly one function or method in one non-test Python file (from the fix patch).
2. The project installs in a conda environment on H: with the Python version BugsInPy gives for the bug, on this
   Windows machine, from the project's own requirement files.
3. The developer's bug-revealing test fails on the buggy and passes on the fixed checkout, twice each.
4. The changed function with its module's imports fits in 6,000 tokens of prompt.

## 4. Selection

Projects in a random order (seed `gbe-c1-v1`); within a project, bugs in a random order with the same seed.
Eligible bugs are taken until 8 per project; the selection stops at 30 bugs or when every project has been
tried. Every attempted project and bug is listed with the step at which it left, including installation
failures. Bugs where generation yields no revealing test stay in the sample.

## 5. Requirement for the judge (independent of the code)

The docstring of the changed function in the buggy version plus the first line of the fix commit's message, with
any code removed. Written to `data/c1/specs/<bug>.txt` for every selected bug before any model call.

## 6. Pipeline

- Generation: Qwen2.5-Coder 7B through the frozen Ollama 0.40.1, temperature 0, seed 0, the Phase 2 code-input
  prompt, plus one added instruction that names the module to import the function from. Any other prompt change
  is listed in section 9.
- Program versions: the buggy and the fixed checkout (the fixed one is the control for false reports, as in the
  main runs).
- Execution: each generated test file runs with the project's pytest inside its environment, from the project
  root, with the same per-test time limit as Phase 2 (raised to 30 s if the project's own test start-up needs
  it, recorded).
- Policies P1 to P4 with the Phase 2 prompts and judge v2b; the judge sees the requirement of section 5.
- Labels: every test is run twice on the buggy and twice on the fixed checkout (REVEALS, ENCODES, NEUTRAL, BROKEN,
  FLAKY), after the pipeline has finished.

## 7. Reported

Per bug and pooled: initial signal (a revealing test exists), fates of revealing tests per policy, fix-blocking
programs per policy and what overwrite adds over discard, triage reports and false reports (test and program
level), with cluster-bootstrap intervals over bugs where the counts allow; the attrition table; the per-bug list.
The result is reported next to the benchmark results whatever it shows.

## 8. Not done

No second model unless time allows (then Qwen3.5 9B, same settings, reported separately); no mutation analysis on
these projects.

## 9. Changes after fixing the protocol

1. 19 October 2026, before any installation: the environments use python.org's official CPython builds from
   NuGet (package `python`, extracted on H:) instead of conda, because conda 4.10.3 on this machine cannot reach
   repo.anaconda.com (HTTP 000) while other HTTPS downloads work. The pinned versions exist there except 3.6.9,
   for which 3.6.8 is used (13 of the 266 step-1 bugs). Installation follows BugsInPy's own `bugsinpy-compile`:
   a virtual environment with that Python, each line of the bug's requirements installed on its own (a failing
   line is logged and skipped), the bug's setup script if any, PYTHONPATH set as in its bug.info, and the
   developer's test command from run_test.sh run from the project root.
2. 19 October 2026, before the installation run (one bug, httpie-3, was installed once to test the script; it is
   redone from scratch in the run): steps 2 and 3 are made operational as follows, in `analysis/c1_install.py`.
   (a) Checkouts as in bugsinpy-checkout: the buggy checkout is the buggy commit with the developer's test files
   from the fixed commit; the fixed checkout is the same plus the developer's fix patch (bug_patch.txt), so the two
   differ only by the patch. (b) One virtual environment per checkout; setup.sh lines that fail are logged and do
   not stop the install, as in BugsInPy; requirement lines that install the project itself are skipped (the
   checkout is on PYTHONPATH). (c) The test command runs with the environment's Python: pytest, py.test and tox as
   `python -m pytest` with the same arguments; PYTHONUTF8=1 so files are read as UTF-8 as on BugsInPy's Linux
   setup. (d) Step 2 fails when an environment cannot be created or the developer test on the fixed checkout
   fails with an import error (project or dependency not importable); step 3 passes when the buggy run fails with
   tests run and the fixed run passes, in the order buggy, fixed, buggy, fixed. (e) A project whose first 3
   attempted bugs fail step 2 is not tried further and its remaining bugs are reported as not tried. (f) Limits:
   15 minutes per requirement line and per test command, 30 per setup line. (g) The work directory is
   <work>, because the paper folder's path contains spaces that old build tools break on. (h) C extensions are
   built with the installed Visual Studio Build Tools 2022 (MSVC 14.37, Windows SDK 10.0.20348, on H:), which
   the Python builds find through vswhere. (Corrected on 19 October during the first bug, spaCy-2: the first
   version of this item said the machine had no compiler, from a search of the default C: paths only; the run
   was not changed, since the compiler had been found and used from the start.)
   (i) The NuGet 3.7.3 build lacks the venv and ensurepip modules; they are copied from the 3.7.4 build, which
   bundles the same pip (19.0.3) and setuptools (40.8.0) that 3.7.3 shipped.
3. 19 October 2026, after 3 bugs of the run (spaCy-2 eligible, spaCy-6 done, spaCy-4 interrupted): (a) a
   requirement line, or a pip line of setup.sh, that fails is retried once with `--prefer-binary`. Reason:
   spaCy-6 pins ranges such as `preshed>=3.0.2,<3.1.0`; pip now picks the newest source release in the range,
   whose build needs Cython 3.1, which does not exist for Python 3.7, while the range also holds ready-built
   releases that installed when BugsInPy was made. (b) A buggy-checkout run in which no test ran and the output
   shows an import error counts as a step 2 failure; the first version counted it as step 3 (spaCy-6, whose test
   could not import thinc). spaCy-6 and spaCy-4 are redone under these rules; spaCy-2 had no failing line, so its
   result is the same under both and is kept. (c) Implementation fix found on the redone spaCy-6: a requirement
   line with an environment marker (`pathlib==1.0.1; python_version < "3.4"`) was split into words and always
   failed; it is now passed to pip whole, and inline comments are dropped. spaCy-6 is redone once more. Its
   unpinned `cython` line now resolves to Cython 3, which cannot compile the 2020 spaCy sources; such failures
   from today's resolution of open version ranges are reported as step 2 attrition, not worked around.
   (d) Implementation fix found on cookiecutter-1, whose test command is `tox ...`: run as `python -m pytest`
   (change 2c), it lacked pytest, which tox installs from tox.ini. For a tox command the installer now installs
   the [testenv] deps of the checkout's tox.ini first (each line, with the same retry), as tox does, and runs
   pytest with the developer's arguments. cookiecutter-1 and the interrupted cookiecutter-3 are redone.
   (e) Correction of change 2(a), found on cookiecutter-1, whose fix commit adds a data file the developer test
   reads (tests/test-generate-context/non_ascii.json): both checkouts now receive, from the fixed commit, the
   bug.info test files and every file under a test path that the fix commit adds or changes (test data, fixtures,
   conftest), so the developer test can run on both and the checkouts still differ only by the fix patch.
   bugsinpy-checkout copies all files of the fix commit into the fixed version only, which would make such
   tests fail on the buggy version for a missing file. spaCy-2 and cookiecutter-1 are redone; the four other
   spaCy bugs failed installation, which does not depend on test files, and are kept.
   (f) Found on tornado-4, whose fixed checkout failed because Git for Windows wrote a static file the test
   serves with CRLF endings (28 bytes where the test expects 26): every checkout now has the files as committed
   (LF endings, `core.autocrlf=false`), as on BugsInPy's Linux setup, and the fix patch is applied with LF
   endings (this machine's BugsInPy clone stores it with CRLF; the stored version is the fallback). The 18 bugs
   eligible at that point were re-tested on rewritten LF checkouts in their existing environments, four runs
   each, and all 18 stayed eligible (their CRLF runs are kept in the result files); tornado-4 is redone in
   full. (g) A unittest command counts as passing only if at least one test ran (exit code 0 alone also
   covers "Ran 0 tests"); all eligible unittest bugs ran one test per command.
4. 19 October 2026, before any model call of the study run (one smoke run on httpie-4 under the separate run ID
   `c1_smoke`, not part of the study): the pipeline adaptations for real repositories.
   (a) The program shown to the model (code input, repair prompts) is the changed function with its module's
   import lines and, for a method, the header line of each enclosing class followed by `...`; the version shown
   is the one under test. For a method, the importable entry point is the outermost class (23 of 30 bugs). No
   changed function is nested in another function.
   (b) Tests run in a scratch folder with the version's own environment and PYTHONPATH; `solution.py` there is a
   two-line shim that re-exports the module (`from <module> import *` and the entry point), so the Phase 2
   prompts' `from solution import ...` stays valid. The added generation instruction of section 6 is the prompt
   `generate_c1_v1`, which is `generate_v1` with one sentence naming the module and the project. Repair and judge
   prompts are unchanged. Tests run with the project's own pytest (5.2.1 to 7.0.1); the 16 tornado environments
   had none (their developer tests use unittest) and received pytest 5.4.3, which does not touch tornado.
   (c) The requirement for the judge (section 5) also contains the function's signature (its def lines), since
   the judge prompt presents "signature and docstring"; the commit line follows the sentence "The fix to this
   function is described as:", with code spans removed. 11 of the 30 functions have no docstring of their own
   (pandas attaches shared docstrings by decorator), so their requirement is the signature and the commit line.
   (d) An exception counts as raised by the program under test (PUT_EXCEPTION, which the triage judge and the
   template repairs act on) when, after the test's last frame, the traceback enters the checkout; in Phase 2 the
   condition was the last frame being solution.py.
   (e) Time limit: the start-up of one trivial test was at most 1.4 s in every environment, so the Phase 2 limit
   of 5 s applies to all 30 bugs.
5. 20 October 2026, during the study run (42 of 60 units done): the run stopped at spaCy-2 (buggy) when a test
   timed out and, after the test process tree was killed, Windows still held its scratch folder, so deleting it
   raised an error. Workspace cleanup now retries for up to 5 s and then leaves the folder. Outcomes are not
   affected (the test was already recorded as TIMEOUT; cleanup runs after the outcome is fixed). The change and
   both file hashes are recorded in runs/c1_qwen25_code/manifest.json (harness_amendments), and the run resumed
   from its 42 finished units with the cached model answers.
6. 20 October 2026, after the first complete study run (`c1_qwen25_code`), found in its review before any
   result was reported: (a) the probe that classifies outcomes read `end_lineno` of the failing assert, which
   exists from Python 3.8 only, so in the 13 bugs with Python 3.6 or 3.7 (tornado, cookiecutter, httpie,
   spaCy) every assertion failure crashed the probe and was recorded as COLLECT_ERROR. Labels (pass or fail per
   version) were unaffected, but the policies act on the outcome kind: overwrite's templates and the triage
   judge apply to ASSERT_FAIL only. The probe now falls back to the largest line number inside the statement.
   (b) All 24 TIMEOUT outcomes of the first executions were cold starts: the first import of the project after
   switching environment exceeded 5 s (pandas, spaCy and others), while the same tests ran normally in the
   evaluation. The start-up measure of change 4(e) took the faster of two runs, a warm start. With a runtime,
   a TIMEOUT is now confirmed by a second execution with the same 5 s limit. Both fixes are no-ops for the
   Phase 2 runs (Python 3.12, no runtime). All 60 units are rerun as `c1_qwen25_code_r2` at the fixed harness,
   with the first run's model answers reused where the prompt is identical (the generated suites therefore
   stay the same); `c1_qwen25_code` is kept on disk as superseded and is not reported.
7. 20 October 2026, after both study runs: (a) as in Phase 2 (finding P2-R1), every evaluated test with a TIMEOUT
   in any of its four executions is re-executed twice per version with a 30 s limit in its environment
   (`analysis/timeout_recheck.py`, now passing the runtime), and the results use the relabelled table
   (tests_rechecked.csv). Qwen2.5: 2 tests rechecked, both relabelled (FLAKY to BROKEN). Qwen3.5: 7 tests
   rechecked, all relabelled; one of them, an unchanged neutral test of pandas-58, had counted as a fix-blocking
   test under overwrite because it timed out twice on a cold fixed environment. The confirming second execution of
   change 6 is not enough for a cold start that lasts longer than 10 s (one trivial test took 20 s afterwards).
   (b) The optional second model of section 8 ran as `c1_qwen35_code` with the same harness; it was stopped once
   before its first unit finished and then resumed.


## 10. Addendum (22 October 2026, before any model call): developers' tests through the policies

Question: on real code, what do the four policies do to a test that is known to reveal the bug? This removes the
generator's reach (section 9, changes 4 to 7: a 7B generator rarely writes a revealing test on these functions)
from the question of what the policies do once such a test exists.

1. Tests: the developer's bug-revealing test commands of the 30 eligible bugs (bug.info, run_test.sh). A test
   enters when it can be lifted into the harness's one-file form and, so lifted, fails on the buggy and passes on
   the fixed checkout in the bug's own environment: a pytest function, or a pytest method of a class without base
   classes whose body does not use `self` or fixtures. unittest tests (tornado) and methods of TestCase classes
   (luigi, httpie-3) do not lift. The dry run of 21 October found 10 such tests in 8 bugs (httpie-4, pandas-23 two
   tests, pandas-58 two, pandas-127, pandas-161, pandas-162, pandas-168, spacy-2); the build script repeats the
   check twice per version with the exact prelude used and keeps only tests that pass it.
2. Lifting: the test function (`self` dropped for methods) becomes the suite's test; the prelude is `from solution
   import *`, the test module's import lines, and the module-level definitions the test refers to (names it uses,
   followed once). Where the test module imports a sibling test helper, the prelude adds the test folder of the
   checkout under test to `sys.path` through the package's own location, so it is the same text on both versions.
3. Pipeline: these suites replace generation (the generated file is written before the run); everything else is
   the Qwen2.5 study run's: prompts, policies P1 to P4, judge v2b with the section 5 requirement, two executions
   per version for labels, the confirming second execution of a time-out, the 30 s recheck after the run. Run ID
   `c1_devtests_qwen25`, both versions of the 8 bugs.
4. Reported: per test, the fate under each policy (dropped, inverted, neutralized, reported) and the edit; per bug,
   fault-enforcing under each policy. With 10 tests in 8 bugs the result is reported as counts and cases, with no
   rates or intervals, beside the generated-test results of section 9.
11. Change 8 (22 October 2026, after the first developer-test run `c1_devtests_qwen25`, before its results were
    reported): 4 of its 10 developer tests (pandas-127, pandas-161, pandas-168, spaCy-2) timed out at their first
    execution, a cold start that outlasted change 6's confirming second execution, so overwrite (which does not
    repair a time-out) dropped them for that reason alone. The harness now runs an unrecorded warm-up (import the
    module once, 120 s limit) before the first execution in an environment other than the previous one. No effect
    on runs without a runtime. The developer-test run is repeated as `c1_devtests_qwen25_r2` with the same seeded
    suites and the first run's model-answer cache; the first run is superseded. The generated-test runs of section
    9 are not repeated: their 6 cold first-execution time-outs (Qwen2.5) were none of them revealing tests.
