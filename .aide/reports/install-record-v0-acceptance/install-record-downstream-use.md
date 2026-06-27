# InstallRecord v0 Downstream Use

`InstallRecord v0` may be used by downstream distribution objects only as
install-state metadata and evidence.

## May Rely On

- `MigrationRecord` may cite InstallRecord refs when recording state transition decisions.
- `UpdatePlan` may cite InstallRecord refs when comparing current installed state to a candidate distribution.
- `RollbackBundle` may cite InstallRecord refs when identifying prior installed state that needs reversible evidence.
- `UpdateReceipt` may cite accepted InstallRecord refs when a future reviewed apply records what happened.

## Must Not Infer

- No downstream object may infer that install apply has happened from an InstallRecord generated in this source repo.
- No downstream object may treat source-generated InstallRecord reports as target repository truth.
- No downstream object may infer target scan authority from InstallRecord acceptance.
- No downstream object may overwrite project-owned, local-only, preserved legacy, unknown, or never-touch state based only on InstallRecord presence.
- No downstream object may treat this acceptance as migration apply, update apply, rollback apply, uninstall apply, release readiness, public package readiness, or canary authority.
