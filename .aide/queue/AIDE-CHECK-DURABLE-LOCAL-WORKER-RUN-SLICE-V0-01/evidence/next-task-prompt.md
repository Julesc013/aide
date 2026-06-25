# Next Task Prompt

```text
Create and process AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01.

Repo truth outranks this prompt. Preserve all prior build and check evidence.

Repair only the material finding from
AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01:

event_record_result_consistency

The fixture report records host_result: PASS, but the committed durable
WorkerRun EventRecord payload records spec.payload.result: null. Update the
durable WorkerRun report/event generation so EventRecord payload result
truthfully preserves the observed host result.

Do not widen the slice. Do not add a general worker harness, autonomous AI
worker, remote ExecutionHost, scheduler, leases, persistent daemon, Workbench
or MCP runtime, provider/model calls, network calls, preview/apply/rollback,
transaction approval, repository mutation, branch/worktree automation, GitHub
mutation, release, or promotion.

Stop at needs_review and recommend exactly:

AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01
```
