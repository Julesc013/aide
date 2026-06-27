# MigrationRecord v0 Downstream Use

`MigrationRecord v0` may be used by downstream objects only as migration decision metadata.

## May Rely On

- `UpdatePlan` may cite MigrationRecord refs when planning compatibility transitions.
- `RollbackBundle` may cite MigrationRecord refs when recording reversal prerequisites.
- `UpdateReceipt` may cite MigrationRecord refs after a future reviewed apply records what happened.

## Must Not Infer

- No downstream object may infer migration apply from MigrationRecord acceptance.
- No downstream object may treat source-generated migration reports as target truth.
- No downstream object may bypass OwnershipLedger preservation rules or InstallRecord evidence requirements.
- No downstream object may treat this acceptance as UpdatePlan acceptance, rollback readiness, release readiness, or canary authority.
