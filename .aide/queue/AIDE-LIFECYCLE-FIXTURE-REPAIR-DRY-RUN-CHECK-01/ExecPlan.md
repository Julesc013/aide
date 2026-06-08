# ExecPlan: AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01

## Objective

Independently review `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` and checkpoint the repair dry-run evidence. The checkpoint verifies the missing-marker and malformed-marker repair scenarios, generated repair plans, generated repair plan reports, expected-state README fallback evidence, missing static expected repair report refs, path boundaries, managed-section marker evidence, hash references, drift-context evidence, no-apply proof, scoped executor interlock, capability labels, and forbidden operations.

## Scope

Allowed writes are limited to this checkpoint task directory, `.aide/queue/index.yaml`, `.aide/context/latest-task-packet.md`, and deterministic status/validation report refreshes. Repair dry-run reports, generated repair plans, generated repair plan reports, expected-state README files, fixture targets, lifecycle schemas, scoped transaction executor source, managed-section implementation, lifecycle repair apply surfaces, and lifecycle apply surfaces are read-only.

## Review Model

The review is static and report-only. It may parse JSON and queue metadata, compare scenario IDs and expected statuses, inspect path and hash references, inspect target marker counts, inspect expected-state README fallback evidence, and rerun local validation/status commands. It must not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, GitHub mutation, provider/model calls, Gateway calls, network calls, release publication, or broad active-repo apply.

## Checkpoint Result

Disposition is `ACCEPTED_WITH_NOTES`. Both repair scenarios are coherent and no prohibited operation is evidenced. The missing static expected repair report refs for `repair-plan-missing-marker` and `repair-plan-malformed-marker` are real evidence gaps, but they do not block this checkpoint because generated plan report evidence, expected-state README fallback evidence, marker-count checks, path checks, preimage hash checks, no-apply proof, and scoped executor interlock evidence are present.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` as the next smallest safe lifecycle WorkUnit. It reviews rollback-compatible record examples and rollback evidence before rollback dry-run or any fixture apply gate. It does not authorize rollback apply, uninstall apply, fixture apply, active repo apply, target repo apply, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
