# Rollback Record Proof

Task: AIDE-APPLY-00-transaction-model

## Added Coverage

- `.aide/apply/rollback-record.schema.json`
- `.aide/examples/apply/rollback-record.example.json`
- `docs/reference/rollback-records.md`
- `.aide/reports/transaction-fixture-plan.json`

## Required Concepts

- Transaction id and operation id linkage.
- Reverse operation class.
- Preimage and postimage references.
- Restore content reference.
- Rollback safety gates.
- Verification evidence references.
- Review gate status.

## Boundary

Rollback records are evidence and planning artifacts in AIDE-APPLY-00. They do not authorize rollback apply, overwrite, deletion, target mutation, managed-section removal, or branch mutation.
