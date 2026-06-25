# AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01

Create and process `AIDE-ACCEPT-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

Acceptance-only. Do not repair implementation.

Accept exactly:

```text
local_process_execution_host_fixture_v0
```

Accepted meaning:

AIDE has a bounded fixture-backed LocalProcessExecutionHost reference slice that
can launch exactly one allowlisted local reference worker through the accepted
RegisteredProcessExecutionProvider v0, preserve raw event evidence, persist
verified content-addressed fixture artifacts, project WorkerRun lifecycle state,
and preserve the source checkout within declared probe coverage.

Do not accept arbitrary command execution, generic worker harness behavior,
autonomous workers, Service/runtime behavior, Workbench/MCP behavior,
provider/model/network calls, preview/apply/rollback, source or target
repository mutation, branch/worktree automation, GitHub mutation, release, or
promotion.

Recommend exactly:

```text
AIDE-BUILD-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01
```
