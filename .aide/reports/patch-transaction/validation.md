# PatchTransaction Validation Report

- result: `PASS_WITH_WARNINGS`
- schema_loaded: `true`
- schema_helper_alignment_status: `PASS`
- record_valid: `true`
- scope_valid: `true`
- deterministic_projection: `true`
- source_artifacts_mutated: `false`
- apply_performed: `false`
- target_mutated: `false`
- approval_granted: `false`
- trusted: `false`
- recommended_next_task: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`

## Warnings

- PatchTransaction is schema/projection/validation only; no apply engine exists.
- Policy evaluation, approval, admission, trust, artifact resolution, VCS reachability, and runtime behavior remain absent.
- Inherited operational-health warning debt is retained: report volume, report ambiguity, generated-output provenance, one stale-context OKF finding, four Reconciler warnings, and queue readability debt.
- ConformanceResult refs are evidence links only and do not grant admission or trust.
