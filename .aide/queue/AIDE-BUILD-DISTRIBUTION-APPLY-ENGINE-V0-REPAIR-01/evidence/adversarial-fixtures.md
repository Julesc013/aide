# Adversarial Fixtures

Added or refined negative scenarios:

- `missing-update-plan-binding`
- `missing-rollback-bundle-binding`
- `mismatched-update-plan-rollback-bundle`
- `predecessor-source-distribution-mismatch`
- `predecessor-project-lock-mismatch`
- `predecessor-ownership-ledger-mismatch`
- `predecessor-install-record-mismatch`
- `predecessor-migration-record-mismatch`
- `run-without-accepted-context`

Each scenario expects `FAILED_VALIDATION`, an explicit refusal code, no successful UpdateReceipt fixture output, no operation execution, canonical fixture preservation, and no real target/source apply.
