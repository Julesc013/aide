# ReferenceID Status

- status: PASS_WITH_WARNINGS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- schema_file_path: .aide/protocol/aide-reference-id.schema.json
- schema_file_exists: true
- helper_path: core/protocol/reference_id.py
- helper_exists: true
- reference_map_exists: true
- capability_label: minimal_reference_id_scheme
- accepted_predecessor: minimal_test_job_schema
- resolution: syntactic_only
- runtime_reference_registry_implemented: false
- resolver_service_implemented: false
- event_record_implemented: false
- okf_knowledge_bundle_implemented: false
- patch_transaction_implemented: false
- adapter_manifest_implemented: false
- target_mutation: false
- active_repo_apply_mutation: false
- branch_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- github_mutation: false

## Reference Scheme

- scheme: aide
- grammar: aide://<kind>/<id>
- fragment_support: true
- identity_rule: Stable IDs are identity; file paths are locators; hashes prove content.

## Known Ref Kinds

- adapter
- artifact
- capability
- checkpoint
- conformance-profile
- conformance-result
- context-pack
- decision
- event
- evidence
- goal
- patch-transaction
- policy
- queue-task
- report
- schema
- source
- test-job
- wave
- worker-run
- workunit

## Explicit Non-Capabilities

- event_record_implementation
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
- leases
- scheduler
- supervisor
- test_broker_runtime
- async_execution
- worker_execution
- service
- commander
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
- production_readiness
- release_readiness
- broad_autonomous_runtime

## Warnings

- Reference ID Scheme is syntactic/projection-only and does not implement runtime resolution.
- EventRecord, OKF, PatchTransaction, adapter manifests, and ContextPack v2 remain future work.
