# ExecPlan: AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01

## Objective

Independently review rollback-compatible lifecycle fixture record examples and rollback evidence before rollback dry-run, rollback execution, uninstall execution, fixture apply, active repo apply, or target repo apply gates. The checkpoint verifies schema alignment, rollback record examples, generated plan and expected report links, preimage/postimage references, inverse-operation shape, rollback preconditions and stop conditions, manual-content preservation notes, protected-path handling, scoped executor interlock, capability labels, and no-rollback-execution proof.

## Scope

Allowed writes are limited to this checkpoint task directory, `.aide/queue/index.yaml`, `.aide/context/latest-task-packet.md`, and deterministic status/validation report refreshes. Rollback records, generated plans, expected reports, fixture targets, lifecycle schemas, scoped transaction executor source, managed-section implementation, rollback/uninstall implementation, lifecycle apply surfaces, release surfaces, provider/model files, and Gateway files are read-only.

## Review Model

The review is static and report-only. It may parse JSON and queue metadata, compare record IDs and lifecycle plan references, verify rollback record links, recompute hashes for referenced fixture content, inspect preconditions and stop conditions, and rerun local validation/status commands. It must not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, active repo apply, target repo mutation, branch/worktree mutation, GitHub mutation, provider/model calls, Gateway calls, network calls, release publication, or broad active-repo apply.

## Checkpoint Result

Disposition is `ACCEPTED_WITH_NOTES`. The rollback record schema, generic example, install fixture rollback record, upgrade fixture rollback record, generated plan links, expected report links, hash references, inverse operations, rollback preconditions, stop conditions, manual-preservation notes, and protected-path checks are coherent. The evidence is static and review-gated; it is not rollback execution and does not authorize rollback dry-run execution by itself.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` as the next smallest safe lifecycle WorkUnit. It should run report-only/dry-run rollback planning checks against rollback-compatible fixture records without rollback execution, uninstall execution, lifecycle apply, scoped transaction fixture apply, active repo apply, target repo apply, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
