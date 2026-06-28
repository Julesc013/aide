# Accepted Execution Model

Accepted capability:

- fixture-only execution against committed DistributionApplyEngine scenario fixtures;
- temp-workspace-only mutation of copied fixture contents;
- accepted predecessor context validation before temp workspace execution;
- UpdatePlan binding validation;
- RollbackBundle binding validation;
- predecessor ref matching for DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord refs;
- bounded operation execution for accepted fixture operation classes;
- rollback verification for successful fixture runs;
- UpdateReceipt-shaped fixture output for successful fixture runs;
- fail-closed refusal before operation execution for missing or mismatched accepted context.

Accepted result boundary:

- canonical fixtures remain unchanged;
- temp workspaces are not retained;
- refusal cases do not emit successful UpdateReceipt output;
- real target repositories are not scanned or mutated;
- the source repo is not treated as an installed target.
