# ExecPlan: AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01

## Objective

Run static report-only and dry-run uninstall planning checks against lifecycle fixture uninstall scenarios. The checks review generated uninstall plans, generated plan reports, expected state, available expected reports, hash references, manual preservation, broad-delete blocking, protected paths, scoped executor v0 limitations, no-execution flags, and capability labels.

## Scope

Allowed writes are limited to this task directory, `.aide/reports/lifecycle-fixture-uninstall-dry-run/**`, queue index, latest task packet, and deterministic status/validation report refreshes. Generated plans, expected reports, fixture targets, lifecycle schemas, scoped transaction executor source, managed-section implementation, lifecycle apply surfaces, provider/model/Gateway files, release files, and target repositories are read-only or protected.

## Check Model

The check model is static and report-only. It may parse JSON, compare fixture metadata and generated plan reports, compute SHA-256 hashes for referenced static fixture files, inspect broad-delete blockers, and confirm no-execution flags. It must not implement or run uninstall apply, rollback apply, rollback execution, lifecycle apply, scoped transaction apply against fixture targets, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, provider/model calls, Gateway calls, GitHub mutation, network calls, release publication, broad active-repo apply, broad deletes, or broad moves.

## Uninstall Scenarios

- `uninstall-manual-preserved`
- `broad-delete-blocked`

Install apply, upgrade apply, lifecycle repair apply, rollback execution, uninstall execution, fixture apply, active repo apply, target repo adoption, Gateway/provider/network work, release work, and broad active-repo apply remain deferred or prohibited.

## Result

Result is `PASS_WITH_WARNINGS`. `uninstall-manual-preserved` has a generated dry-run plan, generated plan report, matching manual-file preservation hash evidence, and static expected state, but it lacks a static expected report ref. `broad-delete-blocked` has a generated report-only plan, generated plan report, static expected report, and explicit `BLOCKED_BROAD_DELETE` evidence. The missing manual-preserved static expected report ref is non-blocking for this dry-run task but repair-worthy before apply-gate closure.

## Next WorkUnit

Select `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01` as the next smallest safe WorkUnit. It is an independent checkpoint and does not authorize uninstall apply, uninstall execution, rollback execution, lifecycle apply, scoped transaction fixture apply, active repo apply, target repo mutation, release work, provider/model/Gateway/network calls, or broad active-repo apply.

## Review Gate

Stop at `needs_review`.
