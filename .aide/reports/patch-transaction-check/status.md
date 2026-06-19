# PatchTransaction Check Status

Result: `FAILED_VALIDATION`

Checked task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`

Checked commit: `2559b1dbc528992451193d942bff741e8cb0a0a7`

The independent check confirmed the build source chain, task evidence,
artifact digest binding, report consistency, lifecycle/no-apply boundaries,
unsupported execution subcommand closure, and canonical repeated projection.

Acceptance is blocked by material path-scope findings:

- `path_scope_drive_prefixed_relative_accepted`
- `path_scope_duplicate_normalization_accepted`

Recommended next task:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
