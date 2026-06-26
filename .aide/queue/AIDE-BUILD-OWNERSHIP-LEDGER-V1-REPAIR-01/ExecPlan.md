# AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01 ExecPlan

## Objective

Repair exactly the five material findings from `AIDE-CHECK-OWNERSHIP-LEDGER-V1-01` without accepting `ownership_ledger_v1` or starting downstream distribution objects.

## Scope

- Expand OwnershipLedger file-entry and managed-section contract fields.
- Add Q43 ownership-class migration projection and CLI surface.
- Add path/case/file/section conflict validation.
- Expand valid and invalid fixture coverage for the repaired contract.
- Regenerate OwnershipLedger and Repair 01 reports/evidence.

## Finding Matrix

The frozen machine-readable matrix is in `finding-matrix.json`.

## Validation Intent

- Focused OwnershipLedger unit tests.
- `ownership-ledger status`, `project`, `validate`, and `migrate-q43`.
- ProjectLock and DistributionManifest regression validation.
- Broad AIDE validation.
- Diff checks, task inspect/evidence, and commit policy.

## Stop Conditions

Stop at `needs_review` with `PASS_WITH_WARNINGS` or `PASS`, material finding count `0`, missing evidence `0`, and recommendation exactly `AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01`.

Do not accept OwnershipLedger v1, begin InstallRecord, implement apply behavior, mutate target repositories, publish releases, call network/provider/model services, or start runtime work.
