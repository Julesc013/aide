# Prompt

Create and process `AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.

Repo truth outranks attached handoffs, generated packets, prior chat, and stale
planning notes.

Accept exactly:

```text
durable_local_worker_run_slice_v0
```

Accepted meaning:

```text
AIDE can compose the accepted local Service foundation, accepted trust
contracts, accepted local trust enforcement, accepted
RegisteredProcessExecutionProvider v0, and accepted LocalProcessExecutionHost
fixture behavior to durably record a bounded fixture-backed local WorkerRun into
temporary local Service state.
```

The accepted slice includes:

```text
WorkUnit
WorkerRun
host outcome
EvidencePacket
EventRecord
monotonic local events
idempotency
artifact metadata
idempotent replay without a second host launch
```

Do not accept:

```text
general worker harness
autonomous AI worker
remote ExecutionHost
scheduler
leases
persistent background Service daemon
Workbench runtime
MCP runtime
provider/model calls
network calls
PreviewSession
DevelopmentTransaction
preview/apply/rollback
transaction approval
source or target repository mutation
branch/worktree automation
GitHub mutation
release or promotion
```

Stop at `needs_review` with:

```text
result: ACCEPTED_WITH_WARNINGS
recommended_next_task: AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01
```
