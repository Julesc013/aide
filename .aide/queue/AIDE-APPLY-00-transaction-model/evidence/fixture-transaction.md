# Fixture Transaction

Task: AIDE-APPLY-00-transaction-model

## Fixture Purpose

The fixture transaction demonstrates the transaction record shape without mutating repository files. It covers staging, preimage, postimage, managed-section operation metadata, verification, ownership boundary, conflict record, safety gates, transaction evidence, and rollback metadata.

## Generated Reports

- `.aide/reports/transaction-fixture-plan.json`
- `.aide/reports/transaction-fixture-plan.md`
- `.aide/reports/transaction-fixture-validation.md`

## Verification Result

- `transaction fixture-plan` - PASS
- `transaction fixture-verify` - PASS, 225 checks
- `transaction validate` - PASS, 489 checks
- `transaction_fixture_plan_golden` - PASS, 7/7
- `transaction_fixture_verify_golden` - PASS, 227/227

## No-Apply Result

The fixture includes planned operation records only. It does not create, edit, delete, rename, move, or patch live repository files.
