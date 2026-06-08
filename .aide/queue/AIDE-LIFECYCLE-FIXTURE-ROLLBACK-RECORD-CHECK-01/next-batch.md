# Next Batch

Selected next task: `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`

Goal: Run report-only/dry-run rollback planning checks against rollback-compatible fixture records, without rollback execution or scoped transaction fixture apply.

Why selected:

- This checkpoint disposition is `ACCEPTED_WITH_NOTES`.
- Rollback-compatible records are coherent enough to support a future rollback dry-run review.
- Rollback dry-run is the smallest safe next lifecycle WorkUnit before rollback execution, uninstall execution, fixture apply, active repo apply, or target repo apply gates.
- The task remains report-only/dry-run and does not widen authority.

Prerequisites:

- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`
- `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`

Allowed paths should be limited to the future rollback dry-run task directory, rollback dry-run report outputs if authorized, queue index/latest task packet updates if policy requires, and deterministic validation report refreshes.

Forbidden operations remain install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claims, and release-ready claims.

Do not execute the selected task in this checkpoint.
