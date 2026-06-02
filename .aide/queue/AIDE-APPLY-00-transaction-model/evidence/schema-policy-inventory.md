# Schema And Policy Inventory

Task: AIDE-APPLY-00-transaction-model

## Policies

- `.aide/policies/transactional-apply.yaml`
- `.aide/policies/file-operations.yaml`
- `.aide/policies/transaction-safety-gates.yaml`

## Schemas

- `.aide/apply/transaction.schema.json`
- `.aide/apply/file-operation.schema.json`
- `.aide/apply/managed-section-operation.schema.json`
- `.aide/apply/preimage.schema.json`
- `.aide/apply/postimage.schema.json`
- `.aide/apply/staged-change.schema.json`
- `.aide/apply/transaction-verification.schema.json`
- `.aide/apply/rollback-record.schema.json`
- `.aide/apply/ownership-boundary.schema.json`
- `.aide/apply/conflict-record.schema.json`
- `.aide/apply/apply-safety-gate.schema.json`
- `.aide/apply/transaction-evidence.schema.json`

## Examples

- `.aide/examples/apply/transaction.report-only.example.json`
- `.aide/examples/apply/transaction.fixture-only.example.json`
- `.aide/examples/apply/file-operation.create-file.example.json`
- `.aide/examples/apply/file-operation.managed-section.example.json`
- `.aide/examples/apply/managed-section-operation.example.json`
- `.aide/examples/apply/preimage.example.json`
- `.aide/examples/apply/postimage.example.json`
- `.aide/examples/apply/staged-change.example.json`
- `.aide/examples/apply/transaction-verification.example.json`
- `.aide/examples/apply/rollback-record.example.json`
- `.aide/examples/apply/ownership-boundary.example.json`
- `.aide/examples/apply/conflict-record.example.json`
- `.aide/examples/apply/apply-safety-gate.example.json`
- `.aide/examples/apply/transaction-evidence.example.json`

## Docs

- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`
- `docs/reference/managed-section-operations.md`
- `docs/reference/rollback-records.md`

## Inventory Result

The transaction model now has separate policy, schema, example, documentation, command, test, golden-task, and export-pack coverage. All records remain report-only or fixture-only in AIDE-APPLY-00.
