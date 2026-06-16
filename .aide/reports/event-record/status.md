# EventRecord Status

- status: PASS_WITH_WARNINGS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-event-record.schema.json
- schema_file_exists: true
- helper_path: core/protocol/event_record.py
- helper_exists: true
- capability_label: minimal_event_record_schema
- accepted_predecessor: minimal_reference_id_scheme
- event_family_count: 12
- projection_report_exists: true
- recorded: false
- projection_only: true
- runtime_event_store_implemented: false
- event_sourcing_runtime_implemented: false
- append_only_runtime_store_implemented: false
- runtime_event_log_implemented: false
- state_reconstruction_implemented: false
- okf_knowledge_bundle_implemented: false
- reconciler_implemented: false
- capability_manifest_implemented: false
- conformance_profile_implemented: false
- patch_transaction_implemented: false
- adapter_manifest_implemented: false
- context_pack_v2_implemented: false
- runtime_reference_registry_implemented: false
- resolver_service_implemented: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- github_mutation: false
- recommended_next_task: AIDE-CHECK-EVENT-RECORD-SCHEMA-01

## Event Families

- AcceptanceRecorded
- CapabilityDeclared
- ConformanceResultRecorded
- EventRecordProjectionRecorded
- EvidencePacketRecorded
- OKFProjectionRecorded
- PatchTransactionRecorded
- ReconcilerFindingRecorded
- ReferenceIDProjectionRecorded
- TestJobRecorded
- WorkUnitStateChanged
- WorkerRunRecorded

## Explicit Non-Capabilities

- event_sourcing_runtime
- append_only_runtime_store
- runtime_event_log
- state_reconstruction
- scheduler
- leases
- supervisor
- test_broker_runtime
- async_execution
- worker_execution
- service
- commander
- okf_knowledge_bundle
- reconciler
- capability_manifest
- conformance_profile
- patch_transaction
- adapter_manifest
- context_pack_v2
- runtime_reference_registry
- resolver_service
- database_state
- provider_adapters
- branch_worktree_automation
- target_apply
- active_apply
- rollback_execution
- uninstall_execution
- release
- promotion
- github_mutation
- gateway_calls
- network_calls
- model_provider_calls
- target_repo_mutation
- broad_autonomous_runtime
- production_readiness
- release_readiness

## Warnings

- EventRecord is projection-only and does not implement an append-only event store.
- OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, and runtime coordination remain future work.
