# Downstream Use Boundary

Downstream objects may rely on RollbackBundle v0 for:

- accepted UpdatePlan binding;
- prior and candidate ProjectLock refs;
- prior OwnershipLedger and InstallRecord refs;
- source and candidate DistributionManifest refs;
- preimage artifact refs;
- managed file and managed section preimage refs;
- reverse operation records;
- operation-to-rollback mapping;
- validation plan and integrity checks;
- manual-review items, limitations, risk class, and evidence refs.

Downstream objects must not infer:

- rollback apply authority;
- update apply authority;
- install apply authority;
- migration apply authority;
- uninstall apply authority;
- target repository mutation permission;
- target scan authority;
- release readiness;
- canary readiness;
- provider/model/network call permission.

UpdateReceipt may later cite an accepted RollbackBundle only as rollback-preparation metadata for recording future execution results. DistributionApplyEngine remains blocked until fixture-only apply authority is separately built, checked, and accepted.
