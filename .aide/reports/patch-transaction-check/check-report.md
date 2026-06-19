# PatchTransaction Check Report

## Result

`FAILED_VALIDATION`

The build is not ready for acceptance review. It needs one bounded repair task.

## Source Chain

- Branch: `main`
- Live HEAD: `2559b1dbc528992451193d942bff741e8cb0a0a7`
- Checked task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- Build state: `needs_review`
- Build result: `PASS_WITH_WARNINGS`
- Build evidence: `missing_evidence: 0`
- Build recommended next task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`

## Confirmed

- The deterministic sample patch artifact SHA-256 independently recomputes to
  `sha256:5747bd0d486a73c1b363b0f4c8af974b4ee1f24968a53221eba2c89f187b3c5f`.
- Changing artifact bytes changes the digest.
- Transaction, report, and lifecycle references agree across the PatchTransaction reports.
- Generated records preserve no approval, no apply, no target mutation, no rollback, and no trust.
- Unsupported execution subcommands fail closed.
- Canonical repeated projection leaves the report tree byte-identical.
- Source inputs were not changed by projection.

## Material Findings

1. `path_scope_drive_prefixed_relative_accepted`

   The production scope validator accepts `C:repo/file.txt` as valid under
   `C:repo/**`. This is a drive-prefixed relative path and should fail closed
   where repository-relative paths are required.

2. `path_scope_duplicate_normalization_accepted`

   The production scope validator accepts both `src//file.py` and
   `src/file.py` in declared paths. These normalize to the same locator and
   should fail closed as ambiguous.

## Warning Disposition

Deferred capabilities remain warnings, not the acceptance blocker: full JSON
Schema Draft validation, general diff parsing, artifact resolution, VCS
reachability, policy evaluation, approval, apply, rollback, event store,
admission, trust, and runtime.

## Next Task

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
