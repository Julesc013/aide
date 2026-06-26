# AIDE-ACCEPT-PROJECT-LOCK-V0-01 ExecPlan

## Objective

Accept exactly `project_lock_v0` after the ProjectLock build and independent
check both reported zero material findings and zero missing evidence.

## Scope

Allowed outputs are this acceptance task directory,
`.aide/reports/project-lock-v0-accept/`, `.aide/queue/index.yaml`, `PLANS.md`,
and `IMPLEMENT.md`.

Implementation, schema, fixtures, source build reports, source check reports,
release archives, target repositories, and OwnershipLedger work are forbidden.

## Verification Plan

- Inspect the ProjectLock build and check task status.
- Verify the independent check result is `PASS_WITH_WARNINGS`.
- Verify the check material finding count is `0`.
- Verify both source tasks report `missing_evidence: 0`.
- Record the accepted boundary and explicit non-capabilities.
- Run ProjectLock validation, broad AIDE validation, task inspect/evidence, diff
  checks, and commit-policy check.

## Result

`ACCEPTED_WITH_WARNINGS`. The next serialized task is exactly
`AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`.
