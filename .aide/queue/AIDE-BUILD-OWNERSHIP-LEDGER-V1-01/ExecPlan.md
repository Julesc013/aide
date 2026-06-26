# AIDE-BUILD-OWNERSHIP-LEDGER-V1-01 ExecPlan

## Objective

Build proposed `ownership_ledger_v1` after accepted ProjectLock v0.

## Scope

Add a Draft 2020-12 OwnershipLedger schema, deterministic helper, read-only AIDE
Lite CLI verbs, fixture corpus, reports, focused tests, and queue evidence.

## Dependencies

- Accepted `distribution_manifest_v1`
- Accepted `project_lock_v0`

## Verification

- Focused OwnershipLedger tests
- `ownership-ledger status`
- `ownership-ledger project`
- `ownership-ledger validate`
- ProjectLock validation regression
- Broad `aide_lite.py validate`
- Task inspect/evidence
- Diff checks
- Commit-policy check

## Result

`PASS_WITH_WARNINGS`. The next serialized task is exactly
`AIDE-CHECK-OWNERSHIP-LEDGER-V1-01`.
