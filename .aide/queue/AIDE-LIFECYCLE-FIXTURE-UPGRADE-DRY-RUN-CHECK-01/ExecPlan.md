# ExecPlan: AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01

## Objective

Independently review `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` and checkpoint the upgrade dry-run evidence. The checkpoint verifies all three upgrade scenarios, generated upgrade plan reports, static expected reports where present, missing static expected report refs, path boundaries, managed section preservation, drift detection, hash references, no-apply proof, scoped executor interlock, capability labels, and forbidden operations.

## Scope

Allowed writes are limited to this checkpoint task directory, `.aide/queue/index.yaml`, `.aide/context/latest-task-packet.md`, and deterministic status/validation report refreshes. Upgrade dry-run reports, generated upgrade plans, expected reports, fixture targets, lifecycle schemas, scoped transaction executor source, managed-section implementation, and lifecycle apply surfaces are read-only.

## Review Model

The review is static and report-only. It may parse JSON and queue metadata, compare scenario IDs and expected statuses, inspect path and hash references, and rerun local validation/status commands. It must not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, GitHub mutation, provider/model calls, Gateway calls, network calls, release publication, or broad active-repo apply.

## Checkpoint Result

Disposition is `ACCEPTED_WITH_NOTES`. All three upgrade scenarios are coherent and no prohibited operation is evidenced. The missing static expected report ref for `upgrade-manual-preserved` is non-blocking for this checkpoint because generated plan report evidence, static file hashes, managed-section preservation checks, path checks, and no-apply proof are present, but it remains a repair-worthy evidence gap.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` as the next smallest safe lifecycle WorkUnit. It remains report-only/dry-run and does not authorize fixture apply, active repo apply, target repo apply, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
