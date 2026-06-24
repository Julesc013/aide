# Prompt

Create and process
`AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`.

Review `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01` and
`AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`.

Accept only:

```text
execution_host_contract_v0
```

as a projection-only ExecutionHost contract defining descriptor, run binding,
event, artifact, approval, usage, operation vocabulary, false-boundary fields,
and explicit non-capabilities.

Do not accept or implement live ExecutionHost, LocalProcessExecutionHost,
RemoteExecutionHost, worker execution, worker harness, scheduler, Service,
Workbench, provider/model/network calls, PreviewSession,
DevelopmentTransaction, PatchTransaction apply, repository mutation,
branch/worktree mutation, GitHub mutation, release, or promotion.

If accepted, recommend exactly:

```text
AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```
