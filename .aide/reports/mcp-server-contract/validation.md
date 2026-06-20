# MCP Server Contract Validation

- validation_status: `PASS_WITH_WARNINGS`
- schema_file_parsed: `True`
- contract_valid: `True`
- deterministic_projection: `True`
- source_artifacts_mutated: `False`
- secret_like_scan_clear: `True`

## Errors

- none

## Warnings

- MCP server contract is projection-only; no live MCP server or transport exists.
- Resources, prompts, and tools are catalogued and fixture-backed only; they are not served or callable.
- Authorization expectations are declared but OAuth, credentials, PolicyDecision, and CapabilityGrant enforcement are not implemented.
- The preferred future aide://interop contract ReferenceID kind is advisory only; the accepted ReferenceID scheme is not broadened by this task.
- Inherited Interop Exports preview-only limitations and prior report/OKF/Reconciler warning debt remain unresolved.
