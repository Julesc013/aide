# Next Batch

Selected next task: `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`

Goal: Independently review rollback dry-run check reports, rollback record consumption, current-hash checks, inverse operations, stop conditions, manual preservation, protected-path boundaries, no-rollback-execution proof, scoped executor interlock, and capability labels.

Why selected:

- This WorkUnit produced rollback dry-run reports with `PASS_WITH_WARNINGS`.
- Independent review is the smallest safe next step before uninstall dry-run, rollback execution, fixture apply, active repo apply, or target repo adoption gates.
- The task remains report-only/review-only and does not widen authority.

Prerequisites:

- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`
- `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`
- `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`
- `AIDE-APPLY-02-scoped-transaction-executor-v0`

Allowed paths should be limited to the future rollback dry-run checkpoint task directory, queue index/latest task packet updates if policy requires, and deterministic validation report refreshes.

Forbidden operations remain install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claims, and release-ready claims.

Do not execute the selected task in this WorkUnit.
