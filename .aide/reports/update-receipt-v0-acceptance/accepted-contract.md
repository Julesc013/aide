# Accepted UpdateReceipt Contract

UpdateReceipt v0 may record:

- accepted UpdatePlan refs;
- accepted RollbackBundle refs;
- target project identity;
- old and new ProjectLock refs;
- prior and new InstallRecord refs;
- prior and new OwnershipLedger refs;
- source and candidate distribution refs;
- operation receipts;
- skipped operations;
- failed operations;
- changed file and section refs;
- preimage and postimage digests;
- artifact refs;
- validation results;
- approval refs;
- executor refs;
- execution environment metadata;
- warnings, limitations, risk class, evidence refs, explicit non-capabilities, created metadata, and extensions.

UpdateReceipt v0 may not:

- authorize execution;
- perform execution;
- imply apply capability;
- mutate target repositories;
- claim release readiness;
- replace UpdatePlan, RollbackBundle, OwnershipLedger, InstallRecord, or ProjectLock authority.
