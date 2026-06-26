# AIDE-CHECK-OWNERSHIP-LEDGER-V1-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-OWNERSHIP-LEDGER-V1-01` without repairing
implementation, accepting `ownership_ledger_v1`, or beginning InstallRecord.

## Scope

Allowed changes are limited to this check task, the OwnershipLedger check
reports, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Review Method

- Verify live queue state and predecessor evidence.
- Inspect the schema, helper, CLI registration, tests, fixtures, reports, and
  task-local self-hosted turn files.
- Recompute the ledger digest independently.
- Probe field coverage, Q43 migration, duplicate path and case collision
  behavior, and fixture coverage.
- Run focused and broad validations.

## Result

`REQUEST_CHANGES`.

Five material findings remain. The check recommends exactly
`AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01` and stops the serialized wave.
