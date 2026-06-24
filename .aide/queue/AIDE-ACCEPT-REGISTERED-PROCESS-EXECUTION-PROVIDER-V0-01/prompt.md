# AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01

Create and process `AIDE-ACCEPT-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.

Accept exactly:

```text
registered_process_execution_provider_v0
```

Accepted meaning: deterministic, pre-registered, shell-free local process
capability execution with immutable specs, precondition checks, bounded
timeout/output capture, stream scrubbing, state-probe hooks, decoder hooks,
`ProcessExecutionReceipt`, `CapabilityOutcome`, and fail-closed behavior.

Do not accept arbitrary command execution, worker execution, ExecutionHost,
provider/model/network calls, Service/runtime behavior, Workbench behavior,
preview/apply/rollback, repository mutation, branch/worktree automation, GitHub
mutation, release, or promotion.

Stop at `needs_review` and recommend exactly:

```text
AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01
```
