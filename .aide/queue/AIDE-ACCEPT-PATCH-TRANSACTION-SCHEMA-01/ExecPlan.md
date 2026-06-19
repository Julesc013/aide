# AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01 ExecPlan

## Objective

Consolidate the live PatchTransaction build/check chain and determine whether
the minimal schema-only capability can be accepted.

## Scope

- Review live queue authority, build task state, check task state, and evidence.
- If the check passed, write bounded acceptance reports.
- If the check failed, stop as `BLOCKED`, preserve the failed check, and route
  only to the bounded repair task.
- Write task-local evidence and acceptance reports.
- Do not modify PatchTransaction implementation, schema, tests, build/check
  reports, accepted predecessor records, runtime, adapter, provider, host, VCS,
  OKF, or target-repository files.

## Live Disposition

The acceptance precondition is not met. `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
has result `FAILED_VALIDATION` and recommends
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

## Milestones

- Live queue and worktree verified.
- Build and check task evidence inspected.
- Failed check preserved.
- Acceptance reports written as blocked consolidation records.
- Task-local evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Exit Criteria

The task exits with `BLOCKED`, no accepted PatchTransaction capability, no
implementation change, no forbidden operation, complete evidence, and exactly
one recommended next task:
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
