# ExecPlan

## Objective

Create a reviewed authority decision for exactly one future fixture-scoped managed-section apply attempt.

## Scope

This task is authority-only. It may inspect gate evidence, the blocked apply task, fixture plan/report/rollback records, hash state, and executor readiness. It may write authority queue artifacts and reports. It must not execute apply or mutate fixture targets.

## Result

Disposition: `AUTHORIZE_EXACT_FIXTURE_APPLY`

The authorization applies only to future task `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01` or a task-local retry named `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01-RETRY`, and only for one fixture file:

`.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md`

No mutation was performed by this authority task.
