# Validation

Validation completed for the check task.

Passing validation:

- Python compile checks passed for DistributionApplyEngine modules, focused tests, and `aide_lite.py`.
- Focused DistributionApplyEngine tests passed.
- `distribution-apply status` passed.
- `distribution-apply plan --scenario managed-file-update` passed.
- `distribution-apply run --scenario managed-file-update --mode apply-temp` passed.
- `distribution-apply verify` passed.
- Predecessor regression validation passed for DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle, and UpdateReceipt.
- Q43-Q48 no-apply/no-publish validators passed.
- Broad `aide_lite.py validate` passed.

Adversarial validation:

- The check-specific adversarial binding probes failed closed incorrectly and produced the material findings recorded in this task.
