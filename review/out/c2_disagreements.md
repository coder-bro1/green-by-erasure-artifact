# C2 step 4: cases where the raters differ

To settle together. Rater A is Claude, rater B the user. The reader page has the full case.
30 cases.

## C001: WHY A=I B=U; SAYS A=N B=N

feat: surface workflow input schema when running from case

- A's reason: agent's own new test for the schema helper; required set follows the implementation
- B's note: Need the field definition for count to tell whether it should be required.
- https://github.com/TracecatHQ/tracecat/pull/1493

## C003: WHY A=W B=U; SAYS A=N B=N

Remove old permission_allowed() methods, complete migration to new allowed() system

- A's reason: fixture database renamed; same expectation (revised M to W on 17 October: test data changed, per the label guide)
- B's note: The excerpt does not show why these tables belong to restricted_db rather than fixtures.
- https://github.com/simonw/datasette/pull/2533

## C008: WHY A=I B=I; SAYS A=Y B=N

Implement SpinfulParticle and ParticleSet

- A's reason: description says the QuTiP tests were updated for version 5; domain size follows the new design
- B's note: (none)
- https://github.com/netket/netket/pull/2064

## C012: WHY A=I B=U; SAYS A=N B=N

PREVIEW: 🚀 feat: LlamaFarm Enterprise AI Framework - Comprehensive Models, Prompts & RAG System

- A's reason: strategies renamed and sample moved in a large refactor
- B's note: (none)
- https://github.com/llama-farm/llamafarm/pull/32

## C014: WHY A=I B=U; SAYS A=N B=N

Implement pitchbend editor for drum pads

- A's reason: page titles renamed and tests reordered
- B's note: (none)
- https://github.com/charlesvestal/extending-move/pull/476

## C015: WHY A=W B=U; SAYS A=N B=N

Add torch-free radix cache

- A's reason: agent's own new radix-cache tests: first expected the full prefix, then the edge segment, which matches the SGLang design
- B's note: (none)
- https://github.com/marin-community/levanter/pull/1095

## C017: WHY A=I B=E; SAYS A=N B=N

Implement HTML file browser for preset tools

- A's reason: pages now render the new file browser
- B's note: Checking for the browser container no longer checks that sample.wav is listed.
- https://github.com/charlesvestal/extending-move/pull/38

## C025: WHY A=I B=I; SAYS A=N B=Y

Fix issue #2791: Task tools now combine with agent tools instead of overriding them

- A's reason: task tools now combine with agent tools, the fix the PR describes
- B's note: (none)
- https://github.com/crewAIInc/crewAI/pull/2792

## C026: WHY A=I B=I; SAYS A=Y B=N

Update markers to v2 format

- A's reason: ULID regex and marker version changed as described; "refresh changelog and tests"
- B's note: (none)
- https://github.com/jrkropp/open-webui-developer-toolkit/pull/621

## C028: WHY A=W B=U; SAYS A=N B=N

Fix Windows CLI execution issue with subprocess permissions

- A's reason: mocked working directory changed; same expectation (revised M to W on 17 October: test data changed, per the label guide)
- B's note: (none)
- https://github.com/crewAIInc/crewAI/pull/3523

## C030: WHY A=E B=I; SAYS A=N B=N

Fix inferred parameters missing from dataset when explicitly added

- A's reason: standalones 1 to 0 while the comment on the same line still says dac_ch1 is standalone
- B's note: (none)
- https://github.com/microsoft/Qcodes/pull/7240

## C034: WHY A=M B=I; SAYS A=N B=N

Add verbose parameter to recognize_vosk()

- A's reason: expected variable replaced by its literal value
- B's note: (none)
- https://github.com/Uberi/speech_recognition/pull/845

## C039: WHY A=I B=I; SAYS A=N B=Y

Refactor mask handling to use PNG files

- A's reason: masks are now returned as file paths, as described
- B's note: (none)
- https://github.com/sunriseapps/imagesorcery-mcp/pull/6

## C043: WHY A=U B=W; SAYS A=N B=N

Add support for classmethods and staticmethods to @mlflow.trace decorator

- A's reason: traced output changes from a dict to the bare value; not explained
- B's note: (none)
- https://github.com/mlflow/mlflow/pull/15839

## C045: WHY A=I B=I; SAYS A=Y B=N

Standardize Stage Naming Convention: CamelCase classes, snake_case identifiers

- A's reason: stage names converted to snake_case as listed in the description
- B's note: (none)
- https://github.com/NVIDIA-NeMo/Curator/pull/987

## C048: WHY A=E B=I; SAYS A=N B=Y

Libs: Parts: Fix trait parsing for footprint names containing commas (Issue #1278)

- A's reason: comma sanitisation is the fix, but the last change also turns dots into underscores in footprint names without explanation
- B's note: (none)
- https://github.com/atopile/atopile/pull/1438

## C060: WHY A=I B=I; SAYS A=N B=Y

Security Audit: Fix Critical IP Spoofing and Multiple Vulnerabilities

- A's reason: security fixes reject requests with 400 and 401 as described
- B's note: (none)
- https://github.com/FarisZR/knocker/pull/8

## C061: WHY A=I B=U; SAYS A=N B=N

feat(AliESA) 阿里云边缘安全加速 DNS provider support

- A's reason: agent's own tests for the new provider
- B's note: (none)
- https://github.com/NewFuture/DDNS/pull/498

## C064: WHY A=I B=M; SAYS A=N B=N

Add flexible modbus payload decoding

- A's reason: decoded values are now floats
- B's note: [500] and [500.0] compare equal here; this assertion does not check the numeric type.
- https://github.com/tomquist/b2500-meter/pull/134

## C067: WHY A=U B=E; SAYS A=N B=N

feat: add tool estimation config and rate limiting infrastructure

- A's reason: billing PR now expects a generic service error and a CSP without Stripe; unclear
- B's note: (none)
- https://github.com/wshobson/maverick-mcp/pull/24

## C069: WHY A=I B=U; SAYS A=N B=N

Add support for data-translate-ignore attribute and translate:off/on comments in HTML translation

- A's reason: agent's own tests for the new ignore feature, partly reordered
- B's note: (none)
- https://github.com/translate/translate/pull/5760

## C072: WHY A=E B=U; SAYS A=N B=N

fix(backend): prevent duplicate graph executions across multiple executor pods

- A's reason: lock tests now expect try_acquire to return None and the lock key to be absent after acquiring; contradicts what a lock should do, not explained
- B's note: (none)
- https://github.com/Significant-Gravitas/AutoGPT/pull/11008

## C073: WHY A=W B=U; SAYS A=N B=N

Simplify test subtitle helper generation

- A's reason: new test-data helper builds batches with three lines
- B's note: (none)
- https://github.com/machinewrapped/llm-subtrans/pull/371

## C074: WHY A=W B=U; SAYS A=N B=N

Optimize GitHub Actions workflows with pytest-testmon

- A's reason: timing thresholds follow shorter sleeps in the test
- B's note: (none)
- https://github.com/Metta-AI/metta/pull/2484

## C076: WHY A=W B=W; SAYS A=Y B=N

Autodetect GPUs

- A's reason: GPU fixture now marks GPU 1 busy; "keep the GPU manager tests green"
- B's note: (none)
- https://github.com/Ziems/arbor/pull/109

## C080: WHY A=M B=M; SAYS A=N B=Y

Finalize and Test `optiland.environment` Subpackage

- A's reason: variable renamed
- B's note: (none)
- https://github.com/HarrisonKramer/optiland/pull/342

## C081: WHY A=I B=U; SAYS A=N B=N

Add dynamic version control to Olive documentation based on Git tags

- A's reason: agent's own tests for version detection
- B's note: (none)
- https://github.com/microsoft/Olive/pull/1897

## C085: WHY A=I B=W; SAYS A=N B=N

Add IPublish interface and PublishBase

- A's reason: agent's own tests for the new base class with a dummy subclass
- B's note: (none)
- https://github.com/swarmauri/swarmauri-sdk/pull/1478

## C086: WHY A=I B=E; SAYS A=N B=N

feat: implement hierarchical agent delegation with allowed_agents parameter

- A's reason: error messages of the new delegation check
- B's note: An unrelated error can now pass the success check as long as it lacks the words authorization error.
- https://github.com/crewAIInc/crewAI/pull/2070

## C100: WHY A=I B=I; SAYS A=N B=Y

Trim example scripts

- A's reason: job count follows the added example metric batches
- B's note: (none)
- https://github.com/andrewm4894/anomstack/pull/193

