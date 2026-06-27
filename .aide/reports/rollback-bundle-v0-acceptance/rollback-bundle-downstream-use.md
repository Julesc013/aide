# RollbackBundle v0 Downstream Use

Downstream objects may use accepted RollbackBundle v0 as:

- a rollback-preparation metadata source;
- a source of prior ProjectLock, OwnershipLedger, and InstallRecord refs;
- a source of preimage artifact refs and preimage digests;
- a source of reverse operation records;
- a source of operation rollback mapping;
- a source of validation plan and integrity check requirements;
- a source of manual-review items, limitations, risk class, and evidence refs.

Downstream objects may not use RollbackBundle v0 as:

- rollback apply authority;
- update apply authority;
- install apply authority;
- migration apply authority;
- uninstall apply authority;
- target repository mutation authority;
- target scan authority;
- release readiness;
- canary readiness;
- provider/model/network call authority.

UpdateReceipt v0 may later cite accepted RollbackBundle v0 only as preparation metadata for recording execution results. DistributionApplyEngine remains blocked until fixture-only apply authority is separately built, checked, and accepted.
