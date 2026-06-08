# Rollback Record Consumption Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/rollback-record-consumption-checks.json`

Result: `PASS_WITH_WARNINGS`

Records consumed:

- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/upgrade-v2.rollback.json`

Schema/version result: `PASS`

Reference result: `PASS`

Execution claim result: `PASS`

Evidence reference result: `PASS`

Warning:

- The generic lifecycle rollback record is example-only and uses placeholder hashes and fixture-content refs. It is not classified as concrete rollback dry-run input.

No rollback record files were mutated.
