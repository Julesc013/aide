# A2A Agent Card Contract Validation

- validation_status: `PASS_WITH_WARNINGS`
- schema_file_parsed: `True`
- contract_valid: `True`
- A2A specification release: `1.0.0`
- A2A protocol version: `1.0`
- official_advertised_skill_count: `0`
- candidate_skill_count: `4`
- callable_skill_count: `0`
- deterministic_projection: `True`
- source_artifacts_mutated: `False`
- secret_like_scan_clear: `True`

## Errors

- none

## Warnings

- A2A Agent Card contract is projection-only; no live endpoint or registration exists.
- A2A Agent Card is a standards-clean local fixture; full vendored official A2A schema validation remains future work.
- Candidate skills are retained as AIDE metadata only and are not advertised as official A2A skills.
- Authentication, authorization, PolicyDecision, CapabilityGrant, and credential handling are intentionally absent.
- Inherited Interop Exports preview-only limitations and prior report/OKF/Reconciler warning debt remain unresolved.
