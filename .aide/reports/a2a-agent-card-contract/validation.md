# A2A Agent Card Contract Validation

- validation_status: `PASS_WITH_WARNINGS`
- schema_file_parsed: `True`
- contract_valid: `True`
- deterministic_projection: `True`
- source_artifacts_mutated: `False`
- secret_like_scan_clear: `True`

## Errors

- none

## Warnings

- A2A agent-card contract is projection-only; no live endpoint or registration exists.
- Agent-card shape is a local structural subset; full external A2A schema validation remains future work.
- Skills are declared as future read-only discovery candidates only; no task delegation or worker execution exists.
- Authentication, authorization, PolicyDecision, CapabilityGrant, and credential handling are intentionally absent.
- Inherited Interop Exports preview-only limitations and prior report/OKF/Reconciler warning debt remain unresolved.
