# Source Chain Review

Status: `BLOCKED`

The build source chain is present:

- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- result: `PASS_WITH_WARNINGS`
- evidence: `missing_evidence: 0`
- checked build commit: `2559b1dbc528992451193d942bff741e8cb0a0a7`

The independent check is present:

- `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
- result: `FAILED_VALIDATION`
- evidence: `missing_evidence: 0`
- check commit: `83565996d277e0eff07447333c2aea0a726932e6`
- recommended next task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`

This source chain is sufficient to block acceptance. It is not sufficient to
accept PatchTransaction.
