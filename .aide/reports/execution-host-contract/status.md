# ExecutionHost Contract Status

- status: PASS_WITH_WARNINGS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- capability_label: execution_host_contract_v0
- accepted_provider_capability: registered_process_execution_provider_v0
- schema_file_path: .aide/protocol/aide-execution-host.schema.json
- schema_file_exists: true
- schema_validation_mode: minimal_json_schema_subset
- projection_only: true
- execution_host_runtime_implemented: false
- worker_execution_implemented: false
- provider_or_model_calls: none
- network_calls: none
- repository_mutation_performed: false
- recommended_next_task: AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01

## Supported Kinds

- ExecutionHostApproval
- ExecutionHostArtifact
- ExecutionHostContractProjectionReport
- ExecutionHostContractValidationReport
- ExecutionHostDescriptor
- ExecutionHostEvent
- ExecutionHostRunBinding
- ExecutionHostUsage

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

## Explicit Non-Capabilities

- live_execution_host
- local_process_execution_host
- remote_execution_host
- worker_execution
- worker_harness
- worker_process_start
- worker_lease
- scheduler
- supervisor
- provider_model_calls
- network_calls
- service_runtime
- workbench_runtime
- preview_session
- development_transaction
- patch_transaction_apply
- repository_mutation
- branch_worktree_automation
- github_mutation
- release_or_promotion
