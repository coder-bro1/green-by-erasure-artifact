# Policy census: how LLM test generators treat a failing assertion

Source of Table I of the paper (section "Background and Policy Space"). Compiled on 8 and 9 October 2026 from the papers and, where public, their code; copied here from the project's Phase 0 notes, which also contain material not needed for replication.

## How published tools treat a failing assertion

Checked from the papers and, where public, the code. Every quoted passage was matched word for word against its source, and the TestART, YATE and TestGen-LLM passages were checked twice. Policies are named as in the study design: overwrite (P2), free LLM repair (P3), discard (P1), keep as a bug candidate (P4).

| Tool | Venue | Language | What happens to a failing assertion | Green on the code under test at the end? | Ran on buggy code during generation? |
|---|---|---|---|---|---|
| TestART | TOSEM 2026 | Java | Overwrite by template (T2 flip, T3 expected := actual, T4 expect the observed exception), one LLM repair, then discard | Yes | No |
| YATE | arXiv 2025 | Java | Overwrite by rule, then the LLM is told to fix the oracles from the execution (3 tries), then discard | Yes | No |
| MuTAP | IST 2024 | Python | Overwrite: "intended behavior repair" puts the output of the program under test into the assertion | Yes | No: generated on correct reference solutions, then run on buggy student programs |
| CANDOR | TOSEM (DOI 10.1145/3803418) | Java | First step tells the LLM to "use the correct oracle suggested in the log" (an overwrite), then discard; a last step rewrites oracles from the specification and keeps them without re-running | No | Yes: PIT mutants of HumanEvalJava and LeetCodeJava as faulty code |
| ASTER (IBM) | ICSE-SEIP 2025 | Java, Python | Rule-based fix of expected versus actual (mechanism not described), then LLM; tests still failing are returned as a separate set | Main suite yes | No |
| CoverUp | FSE 2025 | Python | Free LLM repair ("Modify or rewrite the test to correct it"), 3 attempts, then discard | Yes | No (Mathews and Nagappan later ran it on buggy code) |
| TestPilot | TSE 2024 | JavaScript | Free LLM repair, one round; the paper's own worked example of a repair is an overwrite; tests still failing are reported but excluded from every metric | In the metrics, yes | No |
| HITS | ASE 2024 | Java | Free LLM repair (up to 10 rounds) plus rules that remove "unnecessary validation", then discard | Yes | No |
| CasModaTest | arXiv 2024 | Java | Free LLM repair told to "generate a new test case to pass the test", then discard | Yes | No |
| Panta | ICSE 2026 | Java | Free LLM repair 3 times, then discard; the next prompt suggests fixing the failed assertion | Yes | No |
| ChatTester | FSE 2024 | Java | Paper: execution failures are not repaired. Code: the LLM regenerates the assertion from the implementation, and tests still failing are cut at the failing line | Code: yes | No |
| ChatUniTest | FSE 2024 demo | Java | Paper: free LLM repair, then discard. Code since March 2024: tests whose only failures are assertion errors are kept unchanged and counted as successes (option `prune`, off by default) | Code: no | No |
| Cover-Agent (open TestGen-LLM) | open source | several | Discard; failures are listed in the next prompt as tests not to repeat | Yes | No |
| TestGen-LLM (Meta) | FSE 2024 Companion | Kotlin | Discard on first failure, no repair | Yes | No |
| ACH (Meta) | FSE 2025 Companion | Kotlin | Discard | Yes | Mutants, against the current version |
| AgoneTest | ICSTW 2025 | Java | Discard the whole failing test class | Yes | No |
| JiT catching (Meta) | arXiv 2026 | not stated | Failures on the parent revision discarded; failures on the new change kept as candidate bugs and ranked by LLM judges | No, by design | Yes: real code changes, parent revision as the oracle |
| TestForge | arXiv 2025 | Python | Agent loop of up to 25 steps that must fix any failing test before exiting; the paper notes assertion errors "often contain expected output, making it easier for the agent to update the tests"; tests still failing are removed before evaluation | Yes | No |
| TELPA | TOSEM (DOI 10.1145/3748505) | Python | No repair: failing tests are kept silently and their coverage counted (32.0 percent of failures are assertion errors) | No | No |
| CodaMosa | ICSE 2023 | Python | Not applicable: LLM assertions are stripped before execution in the evaluated configuration | Yes | No |
| SymPrompt | FSE 2024 | Python | No repair; failures are scored as incorrect generations; the paper assumes the focal method is correct | No | No |
| Siddiq et al. (a study, not a tool) | EASE 2024 | Java | No repair; failing tests are scored as wrong under the stated assumption that the code under test is correct | No | No |
| Pynguin (search-based, contrast) | tool | Python | Assertions recorded from observed behaviour; in LLM-assertion mode, failing LLM assertions are removed | Yes | Not applicable |
| EvoSuite (search-based, contrast) | tool | Java | Assertions recorded from observed behaviour; assertions failing in its final check are commented out | Yes | Shamshiri et al. (ASE 2015): generated on the fixed version, run on the buggy one; 55.7 percent of 357 real faults found |
| Randoop (random, contrast) | tool | Java | Regression assertions from observed behaviour; contract violations kept as "error-revealing tests" | No, for the error-revealing tests | Not applicable |

Counts over the 22 LLM rows:

- 12 can rewrite a failing assertion until it agrees with the code: an expected := actual rule or
  explicit instruction in 4 (TestART, YATE, MuTAP, CANDOR's first step), ASTER's undescribed rule,
  and free LLM repair in 7 (CoverUp, TestPilot, HITS, CasModaTest, Panta, TestForge, ChatTester's
  code).
- 4 discard without repair (Cover-Agent, TestGen-LLM, ACH, AgoneTest).
- 3 keep failing assertions: ChatUniTest's current code (counted as successes), TELPA (kept
  silently), and Meta's catching tests (only for failures on a new code change, ranked by judges).
- 2 score every failure as a wrong test without repairing it (SymPrompt, Siddiq et al.).
- 1 has no LLM assertions at run time (CodaMosa).
- None measures, on code without a trusted earlier version, whether the failures it repaired,
  discarded or kept were bugs.

A later sweep of 2025 and 2026 tools, not included in the counts above, found more of the same:
an explicit overwrite instruction in MutGen (accepted at IEEE TSE) and RUG (ICSE 2025, Rust);
free LLM repair followed by discard in TestWeaver (ICSE 2026, Python) and EvoGPT; and CITYWALK
(TOSEM 2025), which avoids execution-feedback repair on purpose because it can align expected
values with observed outputs. Tools built for bug finding keep failures by design (TestAgent,
SeGa, CASCADE, AUGER, AdverTest); section 4.3 covers the ones that matter for P4.

Free LLM repair and overwriting overlap in practice: TestPilot's worked example, CoverUp's
Figure 7 (a real `assert 13 == 11` that the model then "fixed"), TestForge's remark about expected
output in assertion errors, ChatTester's code and Panta's feedback all steer the model toward the
observed value. The study's change-mode classifier measures how often free repair ends
as an overwrite.

Statements worth citing in the paper:

- At least nine papers state that they assume the code under test is correct or that they build
  regression tests: YATE (section 1), Panta (section 5), Siddiq et al. (section 3.1.3),
  TestGen-LLM (section 2), ACH (section 8), TestPilot (section I), SymPrompt (section 5),
  CoverUp (section 1), TestForge (section 6).
- Two say they cannot tell a wrong test from a bug: TestGen-LLM (section 2) and ChatTester
  (section 5.2, which is why its paper does not repair execution failures). TestForge's
  limitations add that its tests "may fail on the code under test, while exposing bugs in the
  code under test", and it removes them anyway.
- AgoneTest (section V-C) notes that a green suite is a necessary condition for PIT to compute
  mutation coverage. That is the structural core of our metric-blindness argument, said by a tool
  paper.
- TestART's description of T4 says a runtime exception usually means a potential error in the
  code, and the template then makes that exception expected.
- Pynguin's source notes that wrong LLM assertions must be removed because otherwise they would be
  "exported as failing tests", which is the alternative our P4 evaluates.
- ChatUniTest's demo paper shows a kept failing test exposing a defect in a buggy `equals` method
  of Apache Commons, the only tool paper in the census that presents a failing generated test as
  a found bug.

## Sources

- YATE: [arXiv 2507.18316](https://arxiv.org/abs/2507.18316), [yate-java](https://github.com/michaelkonstantinou/yate-java), [replication-study-test-repair](https://github.com/michaelkonstantinou/replication-study-test-repair)
- TestART: [arXiv 2408.03095](https://arxiv.org/abs/2408.03095), [DOI 10.1145/3844945](https://doi.org/10.1145/3844945) (Crossref: ACM TOSEM, online 6 Sep 2026), [code](https://github.com/sikygu/TestART)
- Meta: TestGen-LLM [arXiv 2402.09171](https://arxiv.org/abs/2402.09171); ACH [arXiv 2501.12862](https://arxiv.org/abs/2501.12862); Harden and Catch [arXiv 2504.16472](https://arxiv.org/abs/2504.16472); JiT catching [arXiv 2601.22832](https://arxiv.org/abs/2601.22832)
- Contrast tools: TestPilot [arXiv 2302.06527](https://arxiv.org/abs/2302.06527); Shamshiri et al., ASE 2015, DOI 10.1109/ASE.2015.86; [EvoSuite](https://github.com/EvoSuite/evosuite); [Randoop manual](https://randoop.github.io/randoop/manual/index.html)
- Further census rows: ChatTester [arXiv 2305.04207](https://arxiv.org/abs/2305.04207) and [code](https://github.com/FudanSELab/ChatTester); HITS [arXiv 2408.11324](https://arxiv.org/abs/2408.11324); CasModaTest [arXiv 2406.15743](https://arxiv.org/abs/2406.15743); Siddiq et al. [arXiv 2305.00418](https://arxiv.org/abs/2305.00418); AgoneTest [arXiv 2408.07846](https://arxiv.org/abs/2408.07846); Panta [arXiv 2503.13580](https://arxiv.org/abs/2503.13580) and [code](https://github.com/PANTA-TestAutomation/Panta); CANDOR [arXiv 2506.02943](https://arxiv.org/abs/2506.02943) and [code](https://github.com/qiqiguana/candor); CoverUp [arXiv 2403.16218](https://arxiv.org/abs/2403.16218); CodaMosa [code](https://github.com/microsoft/codamosa); TELPA [arXiv 2404.04966](https://arxiv.org/abs/2404.04966); SymPrompt [arXiv 2402.00097](https://arxiv.org/abs/2402.00097); TestForge [arXiv 2503.14713](https://arxiv.org/abs/2503.14713); Pynguin EMSE 2023 [arXiv 2111.05003](https://arxiv.org/abs/2111.05003)
- Census code: [MuTAP](https://github.com/ExpertiseModel/MuTAP), [CoverUp](https://github.com/plasma-umass/coverup), [qodo-cover](https://github.com/qodo-ai/qodo-cover), [ChatUniTest](https://github.com/ZJU-ACES-ISE/chatunitest-core), [TestPilot](https://github.com/githubnext/testpilot), [ASTER outputs](https://github.com/aster-test-generation/aster), [Pynguin](https://github.com/se2p/pynguin)
