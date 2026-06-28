# Accepted Context Binding

The accepted context model requires accepted predecessor reports for:

- DistributionManifest v1
- ProjectLock v0
- OwnershipLedger v1
- InstallRecord v0
- MigrationRecord v0
- UpdatePlan v1
- RollbackBundle v0
- UpdateReceipt v0

The accepted gate enforces:

- accepted status on predecessor reports;
- zero material findings and zero missing evidence in predecessor acceptance reports;
- matching DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord refs;
- UpdatePlan ref binding;
- RollbackBundle ref binding;
- RollbackBundle-to-UpdatePlan binding;
- operation refs present in the accepted UpdatePlan and RollbackBundle coverage sets.
