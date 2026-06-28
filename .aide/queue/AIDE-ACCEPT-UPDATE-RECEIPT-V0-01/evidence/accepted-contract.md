# Accepted Contract

UpdateReceipt v0 is accepted as a no-apply update-execution receipt contract.

Accepted predecessor dependencies:

- DistributionManifest v1
- ProjectLock v0
- OwnershipLedger v1
- InstallRecord v0
- MigrationRecord v0
- UpdatePlan v1
- RollbackBundle v0

Accepted contract surfaces:

- schema: `.aide/protocol/aide-update-receipt-v0.schema.json`
- helper/projection/validation: `core/protocol/update_receipt.py`
- CLI: `update-receipt status`, `update-receipt project`, `update-receipt validate`
- fixtures: `.aide/fixtures/update-receipt-v0/**`
- reports: `.aide/reports/update-receipt-v0/**`

Accepted meaning:

- records future execution receipt facts from an accepted UpdatePlan;
- binds RollbackBundle, old/new ProjectLock, ownership ledger, install records, distribution refs, operation receipts, skipped operations, failed operations, changed refs, digests, validation results, warnings, limitations, evidence, and explicit non-capabilities;
- does not authorize, perform, retry, or repair any operation.
