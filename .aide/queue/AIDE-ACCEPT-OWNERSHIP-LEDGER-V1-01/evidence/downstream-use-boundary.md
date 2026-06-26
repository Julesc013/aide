# Downstream Use Boundary

`OwnershipLedger v1` is accepted as ownership classification and preservation
truth for later distribution planning objects.

Allowed downstream use:

- `InstallRecord` may cite observed ownership entries and no-apply boundaries.
- `MigrationRecord` may cite Q43 migration dispositions.
- `UpdatePlan` may classify candidate operations by ownership class.
- `RollbackBundle` may cite preimage, digest, and ownership fields.
- `UpdateReceipt` may cite final ownership state after a future reviewed apply.

Forbidden downstream inference:

- no downstream object may infer vendor ownership from path absence;
- no downstream object may overwrite `project_owned`, `project_overlay`,
  `project_generated`, `runtime_generated`, `local_only`, `evidence_only`,
  `preserved_legacy`, `unknown`, or `never_touch` without a later explicit
  reviewed policy;
- no downstream object may treat source latest outputs as target truth;
- no downstream object may treat Q43 migration projection as migration apply;
- no downstream object may treat this acceptance as release, install, update,
  rollback, uninstall, target scan, canary, or public readiness authority.
