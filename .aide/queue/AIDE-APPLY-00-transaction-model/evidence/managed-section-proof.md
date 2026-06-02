# Managed Section Proof

Task: AIDE-APPLY-00-transaction-model

## Added Coverage

- `.aide/apply/managed-section-operation.schema.json`
- `.aide/examples/apply/managed-section-operation.example.json`
- `.aide/examples/apply/file-operation.managed-section.example.json`
- `docs/reference/managed-section-operations.md`

## Required Concepts

- Marker ownership and section id.
- Existing preimage and proposed postimage records.
- Staged replacement content.
- Conflict classification.
- Verification gates before and after a future patch.
- Rollback record requirements.

## Boundary

AIDE-APPLY-00 defines and validates managed-section transaction records only. It does not implement the patcher. AIDE-APPLY-01 is the planned follow-up for a managed-section patcher that must remain review-gated.
