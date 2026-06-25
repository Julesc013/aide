# Prompt

Create and process
`AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`.

Repair only the material finding from
`AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`:

```text
event_record_result_consistency
```

The durable fixture report records `host_result: PASS`, but the committed
EventRecord payload records `spec.payload.result: null`. Update EventRecord
generation so the payload truthfully preserves the observed host result.

Do not widen the slice. Do not add a general worker harness, autonomous AI
worker, remote ExecutionHost, scheduler, leases, persistent daemon, Workbench
or MCP runtime, provider/model calls, network calls, preview/apply/rollback,
transaction approval, repository mutation, branch/worktree automation, GitHub
mutation, release, or promotion.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01
```
