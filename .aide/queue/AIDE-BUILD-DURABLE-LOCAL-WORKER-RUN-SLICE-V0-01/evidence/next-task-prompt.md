# Next Task Prompt

```text
Create and process AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01.

Independently verify AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01.

Confirm the build composes only accepted local Service, accepted trust
contracts, accepted local trust enforcement, accepted RegisteredProcessExecutionProvider
v0, and accepted LocalProcessExecutionHost fixture behavior.

Verify exactly one accepted local reference host run is launched for the valid
fixture, local trust authorization is evaluated and consumed before launch,
the local Service persists WorkUnit, WorkerRun, host outcome, EvidencePacket,
EventRecord, event sequences, idempotency, and artifact metadata, and replay
does not launch a second host run.

Verify reports are deterministic and scrubbed, no .aide.local state is
committed, no accepted source reports are mutated, no arbitrary command,
provider/model, network, Workbench, preview/apply/rollback, repository mutation,
branch/worktree, GitHub, release, or promotion behavior is introduced, and
missing_evidence is 0.

Do not repair implementation in this check task.

If material defects remain, recommend exactly:
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01.

If the build passes, recommend exactly:
AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01.

Stop at needs_review.
```
