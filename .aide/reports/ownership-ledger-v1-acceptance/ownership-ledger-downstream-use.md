# OwnershipLedger v1 Downstream Use

`OwnershipLedger v1` may be used by downstream distribution objects only as
ownership classification and preservation metadata.

## May Rely On

- `InstallRecord` may cite observed ownership entries and no-apply boundaries.
- `MigrationRecord` may cite Q43 migration dispositions.
- `UpdatePlan` may classify candidate operations by ownership class.
- `RollbackBundle` may cite preimage, digest, and ownership fields.
- `UpdateReceipt` may cite final ownership state after a future reviewed apply.

## Must Not Infer

- No downstream object may infer vendor ownership from path absence.
- No downstream object may overwrite project-owned, project-overlay,
  project-generated, runtime-generated, local-only, evidence-only,
  preserved-legacy, unknown, or never-touch entries without a later reviewed
  policy.
- No downstream object may treat source latest outputs as target truth.
- No downstream object may treat Q43 migration projection as migration apply.
- No downstream object may treat this acceptance as release, install, update,
  rollback, uninstall, target scan, canary, or public readiness authority.
