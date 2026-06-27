# UpdatePlan v1 Downstream Use

Downstream objects may use accepted UpdatePlan v1 as:

- a dry-run operation classification source;
- a source of planned operation refs;
- a source of preserved path refs;
- a source of conflict and manual-review refs;
- a source of validation plan and rollback requirement refs;
- a binding surface for accepted DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord refs/digests.

Downstream objects may not use UpdatePlan v1 as:

- update apply authority;
- install apply authority;
- migration apply authority;
- repair apply authority;
- rollback apply authority;
- uninstall apply authority;
- target repository mutation authority;
- target scan authority;
- release readiness;
- canary readiness;
- provider/model/network call authority.

RollbackBundle v0 may cite UpdatePlan rollback requirements, but must independently record recovery metadata and preimage refs. UpdateReceipt v0 may later cite an accepted UpdatePlan only as a prior reviewed plan, not as execution authorization. DistributionApplyEngine remains blocked until fixture-only apply authority is separately built, checked, and accepted.
