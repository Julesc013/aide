# Downstream Use Boundary

Downstream objects may rely on UpdatePlan v1 for:

- current ProjectLock and candidate ProjectLock refs/digests;
- candidate DistributionManifest refs/digests;
- OwnershipLedger refs/digests and ownership classifications;
- InstallRecord and MigrationRecord refs/digests;
- planned operation classes and operation refs;
- managed file and managed section dry-run operations;
- preserved paths and conflict/manual-review records;
- validation plan, rollback requirements, risk class, approval requirements, and evidence refs.

Downstream objects must not infer:

- update apply authority;
- install apply authority;
- migration apply authority;
- repair apply authority;
- rollback apply authority;
- uninstall apply authority;
- target repository mutation permission;
- target scan authority;
- public release readiness;
- canary readiness;
- provider/model/network call permission.

RollbackBundle may cite UpdatePlan rollback requirements but must independently materialize recovery metadata and preimage refs. UpdateReceipt may later cite an accepted UpdatePlan only as a prior plan, not as execution authorization. DistributionApplyEngine remains blocked until fixture-only apply authority is explicitly accepted by later queue gates.
