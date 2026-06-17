# CapabilityManifest Validation

- validation_status: PASS_WITH_WARNINGS
- schema_exists: true
- helper_exists: true
- cli_registered: true
- reports_generated: true
- capabilities_json_valid: true
- capability_index_json_valid: true
- required_capabilities_projected: true
- accepted_capabilities_have_evidence: true
- accepted_with_warnings_preserved: true
- status_semantics_valid: true
- conformance_not_overclaimed: true
- execution_not_overclaimed: true
- reconciler_integration_checked: true
- okf_integration_checked: true
- reference_id_refs_valid: true
- predecessor_compatibility_preserved: true
- overclaiming_check_passed: true
- forbidden_ops_preserved: true
- conformance_implemented: false
- admission_implemented: false
- execution_implemented: false
- runtime: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- recommended_next_task: AIDE-CHECK-CAPABILITY-MANIFEST-01

## Errors

- none

## Warnings

- CapabilityManifest declares capability state but does not prove conformance.
- ConformanceProfile is not implemented.
- ConformanceResult is not implemented.
- Adapter admission is not implemented.
- Adapter execution is not implemented.
- Runtime capability registry is not implemented.
- PatchTransaction is not implemented.
- AdapterManifest is not implemented.
- ContextPack v2 is not implemented.
- Accepted predecessor capabilities preserve accepted_with_warnings rather than flattening to done.
- Stale latest-task-packet drift remains reported; queue truth is canonical.
