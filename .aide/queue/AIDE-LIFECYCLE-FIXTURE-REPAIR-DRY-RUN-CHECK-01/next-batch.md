# Next Batch

Selected next task: `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`

Goal: Independently review rollback-compatible record examples and rollback evidence before rollback dry-run or any fixture apply gate.

Why selected:

- This checkpoint disposition is `ACCEPTED_WITH_NOTES`.
- Missing static expected repair report refs are classified as non-blocking for checkpoint acceptance.
- Rollback-compatible records are the next safety prerequisite before rollback dry-run or any fixture apply gate.
- The task remains review/checkpoint oriented and does not widen authority.

Prerequisites:

- `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`
- `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`

Allowed paths should be limited to the future rollback record checkpoint task directory, queue index/latest task packet updates if policy requires, and deterministic validation report refreshes.

Forbidden operations remain install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claims, and release-ready claims.

Do not execute the selected task in this checkpoint.
