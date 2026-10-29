# C2: restoration cases for reading

One section per merged agent pull request whose changed expected value a later commit restored.

## Hankanman/Area-Occupancy-Detection#71 (OpenAI_Codex), merged 2025-06-23

Title: Refactor overall_probability

PR: https://github.com/Hankanman/Area-Occupancy-Detection/pull/71

Body (start):

```
## Summary
- update `overall_probability` to multiply entity posteriors
- adapt tests for the new complementary logic

## Testing
- `pytest -q`

------
https://chatgpt.com/codex/tasks/task_e_6859a9e2dce0832fb6af6dacbfd7c65e
```

Non-test files changed by the pull request: custom_components/area_occupancy/data/entity.py, custom_components/area_occupancy/utils.py

Restoring commit e12fd76584 on 2025-07-30 by Hankanman:

```
Refactor AreaOccupancyStorage and Entity management

- Introduced EntityFactory for streamlined entity creation from storage and configuration specifications.
- Updated AreaOccupancyStorage to utilize SQLite's INSERT OR IGNORE for efficient batch saving of state intervals.
- Enhanced error handling in DatabaseExecutor for integrity errors.
- Refactored entity management logic to improve synchronization with configuration and validation of entity specifications.
- Adjusted sensor configuration handling to ensure proper mapping and validation of entity types.
```

Files: 6 (3 non-test); non-test files shared with the pull request: custom_components/area_occupancy/data/entity.py

Restored lines:

- `tests/test_data_entity.py`: agent `assert entity.evidence is None`, restored `assert entity.evidence is False`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## Ljzd-PRO/KToolBox#274 (Copilot), merged 2025-07-29

Title: Fix DDoS Guard cookie field names to use new underscore format

PR: https://github.com/Ljzd-PRO/KToolBox/pull/274

Body (start):

```
This PR fixes issue #271 by updating all DDoS Guard cookie names from the old format (`ddg1`, `ddg5`, `ddg8`, `ddg9`, `ddg10`) to the new format (`__ddg1_`, `__ddg5_`, `__ddg8_`, `__ddg9_`, `__ddg10_`).

## Changes Made

- **Updated `ktoolbox/ddos_guard.py`**: Changed all cookie name references and detection logic to use the new underscore format
- **Updated `tests/ktoolbox/test_ddos_guard.py`**: Updated all test cases to verify functionality with the new cookie names
- **Maintained full backward compatibility**: All existing functionality remains intact, only the cookie names have changed

The implementation ensures that DDoS Guard bypass functionality continues to work correctly while using the updated cookie naming convention required by the protection system.

Fixes #271.

<!-- START COPILOT CODING AGENT TIPS -->
---

💡 You can make Copilot smarter by setting up custom instructions, customizing its development environment and configuring Model Context Protocol (MCP) servers. Learn more [Copilot coding agent tips](https://gh.io/copilot-coding-agent-tips) in the docs.
```

Non-test files changed by the pull request: ktoolbox/ddos_guard.py

Restoring commit 4be833b64b on 2025-07-31 by Ljzd-PRO:

```
Revert "Fix DDoS Guard cookie field names to use new underscore format"

This reverts commit 69e711dcdfc314290389a2288b168808157c5e52.
```

Files: 2 (1 non-test); non-test files shared with the pull request: ktoolbox/ddos_guard.py

Restored lines:

- `tests/ktoolbox/test_ddos_guard.py`: agent `assert "__ddg1_" in cookies`, restored `assert "ddg1" in cookies`
- `tests/ktoolbox/test_ddos_guard.py`: agent `assert "__ddg8_" in cookies`, restored `assert "ddg8" in cookies`
- `tests/ktoolbox/test_ddos_guard.py`: agent `assert "__ddg9_" in cookies`, restored `assert "ddg9" in cookies`
- `tests/ktoolbox/test_ddos_guard.py`: agent `assert "__ddg10_" in cookies`, restored `assert "ddg10" in cookies`
- `tests/ktoolbox/test_ddos_guard.py`: agent `assert "__ddg10_" not in manager.cookies`, restored `assert "ddg10" not in manager.cookies`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## Significant-Gravitas/AutoGPT#10965 (Claude_Code), merged 2025-09-23

Title: feat(backend): implement comprehensive load testing performance fixes + database health improvements

PR: https://github.com/Significant-Gravitas/AutoGPT/pull/10965

Body (start):

```
## Summary

This PR implements comprehensive performance fixes for the AutoGPT Platform, addressing critical load testing bottlenecks and database connectivity issues:

### 🚀 Load Testing Infrastructure & Performance Fixes

**Problem:** Platform failed under 100+ RPS load due to database bottlenecks and inefficient API patterns.

**Root Cause Analysis:**
- Database connection pool exhaustion (50 connections/pod limit)
- Unnecessary `/api/auth/user` calls causing repeated database lookups
- Large API payloads (4.6MB for `/api/graphs`, 3.9MB for `/api/executions`)
- Missing user profile caching led to O(n) database queries per request

**Solutions Implemented:**

#### 1. User Profile Caching System
- **Implementation:** Use existing `async_ttl_cache` from autogpt_libs for user lookup optimization
- **Applied to:** `get_or_create_user`, `get_user_by_id`, `get_user_by_email` in `/backend/backend/data/user.py`
- **Performance impact:** Eliminates repeated database lookups, reduces connection pool pressure
- **Cache invalidation:** Automatic cleanup on user updates maintains data consistency

#### 2. Load Test Infrastructure Overhaul
- **k6 Load Testing Suite:** Production-ready tests wi
```

Non-test files changed by the pull request: autogpt_platform/autogpt_libs/autogpt_libs/utils/cache.py, autogpt_platform/backend/.gitignore, autogpt_platform/backend/backend/blocks/__init__.py, autogpt_platform/backend/backend/data/block.py, autogpt_platform/backend/backend/data/graph.py, autogpt_platform/backend/backend/data/redis_client.py, autogpt_platform/backend/backend/data/user.py, autogpt_platform/backend/backend/executor/database.py, autogpt_platform/backend/backend/integrations/webhooks/__init__.py, autogpt_platform/backend/backend/server/external/routes/v1.py, autogpt_platform/backend/backend/server/routers/v1.py, autogpt_platform/backend/backend/server/v2/builder/db.py

Restoring commit 50689218ed on 2025-09-24 by majdyz:

```
feat(backend): implement comprehensive load testing performance fixes + database health improvements (#10965)
```

Files: 36 (34 non-test); non-test files shared with the pull request: autogpt_platform/autogpt_libs/autogpt_libs/utils/cache.py, autogpt_platform/backend/.gitignore, autogpt_platform/backend/backend/blocks/__init__.py, autogpt_platform/backend/backend/data/block.py, autogpt_platform/backend/backend/data/graph.py, autogpt_platform/backend/backend/data/redis_client.py, autogpt_platform/backend/backend/data/user.py, autogpt_platform/backend/backend/executor/database.py, autogpt_platform/backend/backend/integrations/webhooks/__init__.py, autogpt_platform/backend/backend/server/external/routes/v1.py, autogpt_platform/backend/backend/server/routers/v1.py, autogpt_platform/backend/backend/server/v2/builder/db.py, autogpt_platform/backend/backend/util/clients.py, autogpt_platform/backend/backend/util/feature_flag.py, autogpt_platform/backend/backend/util/service.py, autogpt_platform/backend/backend/util/settings.py, autogpt_platform/backend/load-tests/README.md, autogpt_platform/backend/load-tests/core-api-load-test.js, autogpt_platform/backend/load-tests/interactive-test.js, autogpt_platform/backend/load-tests/marketplace-access-load-test.js, autogpt_platform/backend/load-tests/marketplace-library-load-test.js, autogpt_platform/backend/load-tests/scenarios/comprehensive-platform-load-test.js, autogpt_platform/backend/load-tests/single-endpoint-test.js

Restored lines:

- `autogpt_platform/autogpt_libs/autogpt_libs/utils/cache_test.py`: agent `assert result1 == 10`, restored `assert result1 == 3`
- `autogpt_platform/autogpt_libs/autogpt_libs/utils/cache_test.py`: agent `assert result2 == 10`, restored `assert result2 == 9`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## mfat/sshpilot#434 (OpenAI_Codex), merged 2025-09-21

Title: Default HostName to host alias when missing

PR: https://github.com/mfat/sshpilot/pull/434

Body (start):

```
## Summary
- default parsed hostnames to the host token when HostName is omitted so connections have a valid target
- record the host token alongside parsed data and extend tests to cover alias fallback and ssh command generation
- update existing host-without-hostname expectations to reflect the alias fallback behaviour

## Testing
- pytest

------
https://chatgpt.com/codex/tasks/task_e_68d003172d108328a1848e4144b03ded
```

Non-test files changed by the pull request: sshpilot/connection_manager.py

Restoring commit f1b2e39a8f on 2025-09-22 by mfat:

```
Refine hostname handling for alias-only SSH entries
```

Files: 6 (4 non-test); non-test files shared with the pull request: sshpilot/connection_manager.py

Restored lines:

- `tests/test_host_without_hostname.py`: agent `assert conn.hostname == 'example.com'`, restored `assert conn.hostname == ''`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## mfat/sshpilot#445 (OpenAI_Codex), merged 2025-09-22

Title: Ensure host alias persists when hostname blank

PR: https://github.com/mfat/sshpilot/pull/445

Body (start):

```
## Summary
- keep `Connection.host` aligned with the connection alias and update credential cleanup to use alias fallbacks when `hostname` is unset
- adjust password retrieval in the dialog and terminal flows to request stored secrets using whichever identifier is available
- extend test coverage for alias preservation and harden GI stubs so file manager imports succeed during testing

## Testing
- pytest

------
https://chatgpt.com/codex/tasks/task_e_68d00e13f1148328b47e585b877a1b6d
```

Non-test files changed by the pull request: sshpilot/connection_dialog.py, sshpilot/connection_manager.py, sshpilot/terminal.py

Restoring commit f1b2e39a8f on 2025-09-22 by mfat:

```
Refine hostname handling for alias-only SSH entries
```

Files: 6 (4 non-test); non-test files shared with the pull request: sshpilot/connection_manager.py

Restored lines:

- `tests/test_ssh_config_tokenization.py`: agent `assert connection.hostname == "alias"`, restored `assert connection.hostname == ""`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## mfat/sshpilot#446 (OpenAI_Codex), merged 2025-09-22

Title: Handle hosts without explicit hostname

PR: https://github.com/mfat/sshpilot/pull/446

Body (start):

```
## Summary
- ensure `ConnectionManager.parse_host_config` keeps HostName empty when omitted while preserving the alias on `host`
- adjust tokenization tests to expect the empty HostName value and to verify alias fallback behaviour

## Testing
- `pytest tests/test_ssh_config_tokenization.py tests/test_host_without_hostname.py`


------
https://chatgpt.com/codex/tasks/task_e_68d00e1b480083289fcc78df726f7780
```

Non-test files changed by the pull request: sshpilot/connection_manager.py

Restoring commit f1b2e39a8f on 2025-09-22 by mfat:

```
Refine hostname handling for alias-only SSH entries
```

Files: 6 (4 non-test); non-test files shared with the pull request: sshpilot/connection_manager.py

Restored lines:

- `tests/test_ssh_config_tokenization.py`: agent `assert connection.hostname == "alias"`, restored `assert connection.hostname == ""`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

## tyrneh/options-implied-probability#64 (OpenAI_Codex), merged 2025-09-07

Title: Improve put-call parity preprocessing

PR: https://github.com/tyrneh/options-implied-probability/pull/64

Body (start):

```
## Summary
- Build parity conversion on the union of call and put strikes, synthesizing missing legs and returning one call price per strike with diagnostics
- Prefer mid prices when pivoting option quotes and loosen parity detection to require only a single call–put pair
- Correct dividend-yield convention in pricing tests and cover parity edge cases like missing data and fallback paths

## Testing
- `pytest -q`


------
https://chatgpt.com/codex/tasks/task_e_68bdd463db70832293cd5b0edd121fb2
```

Non-test files changed by the pull request: oipd/core/parity.py

Restoring commit c2f00bbd84 on 2025-09-14 by tyrneh:

```
added black76 as a pricing engine
```

Files: 15 (10 non-test); non-test files shared with the pull request: none

Restored lines:

- `tests/core/test_parity.py`: agent `assert len(result) == 3`, restored `assert len(result) == 2`
- `tests/core/test_parity.py`: agent `assert set(result['strike']) == {95, 100, 105}`, restored `assert set(result['strike']) == {95, 105}`

Classification (to fill): REVERT_OF_PR / BUG_HIDDEN_BY_TEST_EDIT / BEHAVIOUR_FLIP_FLOP / OTHER

