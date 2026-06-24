# ExecutionHost Contract Validation

- status: PASS_WITH_WARNINGS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- capability_label: execution_host_contract_v0
- accepted_provider_capability: registered_process_execution_provider_v0
- schema_file_path: .aide/protocol/aide-execution-host.schema.json
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_validation_mode: minimal_json_schema_subset
- schema_helper_alignment_checked: true
- schema_helper_alignment_status: PASS
- projection_only_truthful: true
- capability_execution_distinct: true
- worker_session_contract_defined: true
- explicit_non_capabilities_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true
- execution_host_runtime_implemented: false
- worker_execution_implemented: false
- provider_or_model_calls: none
- network_calls: none
- repository_mutation_performed: false
- recommended_next_task: AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01

## Validation Results

- PASS: .aide/reports/execution-host-contract/projections/execution-host-descriptor.json
- PASS: .aide/reports/execution-host-contract/projections/execution-host-run-binding.json
- PASS: .aide/reports/execution-host-contract/projections/execution-host-event.json
- PASS: .aide/reports/execution-host-contract/projections/execution-host-artifact.json
- PASS: .aide/reports/execution-host-contract/projections/execution-host-approval.json
- PASS: .aide/reports/execution-host-contract/projections/execution-host-usage.json

## Operations

- attach
- collect_artifacts
- create_run
- finish
- interrupt
- probe
- reconcile
- resolve_runtime_approval
- send_input
- stream_events

## Warnings

- ExecutionHost contract v0 is projection-only and does not implement a live host.
- Worker/session execution remains separate from deterministic capability execution.
- LocalProcessExecutionHost is intentionally deferred to the next build after independent check and acceptance.
