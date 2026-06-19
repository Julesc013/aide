# Source Chain Review

Status: `PASS_WITH_WARNINGS`

- build task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- build task result: `PASS_WITH_WARNINGS`
- build task evidence: `missing_evidence: 0`
- failed check task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
- failed check result: `FAILED_VALIDATION`
- failed check evidence: `missing_evidence: 0`
- failed check commit: `8356599` is an ancestor of live `HEAD`
- checked build commit recorded by check report:
  `2559b1dbc528992451193d942bff741e8cb0a0a7`
- failed check material findings:
  - `path_scope_drive_prefixed_relative_accepted`
  - `path_scope_duplicate_normalization_accepted`
- repair task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`
- repair task result: `PASS_WITH_WARNINGS`
- repair task evidence: `missing_evidence: 0`

The failed independent check remains preserved. This repair does not rewrite
build or check evidence.
