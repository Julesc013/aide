# ConformanceProfile Acceptance Non-Capabilities

Accepted capability: `minimal_conformance_profile`.

Accepted behavior:

- versioned ConformanceProfile schema
- profile-scoped ConformanceCase model
- candidate profile projection
- profile and case validation
- profile and case indexes
- required/optional/advisory requirement levels
- fail-closed required-case aggregation policy
- evidence requirement declarations
- versioning and compatibility policy
- CapabilityManifest subject integration
- Track B governance evidence integration
- `conformance-profile status/project/validate` CLI
- deterministic projection

## explicit_non_capabilities

- conformance_result
- conformance_runner
- conformance_execution
- case_execution
- command_execution
- conformance_admission
- automatic_admission
- policy_decision
- profile_activation
- subject_admission_by_conformance
- trust_grant
- adapter_admission
- adapter_execution
- capability_execution
- runtime_capability_registry
- patch_transaction
- adapter_manifest
- context_pack_v2
- scheduler
- leases
- supervisor
- runtime
- service
- commander
- test_broker_runtime
- worker_execution
- provider_adapters
- provider_model_calls
- network_calls
- gateway_calls
- github_mutation
- branch_worktree_automation
- target_repo_mutation
- target_apply
- active_apply
- rollback_execution
- release
- promotion
- production_readiness
- release_readiness
- broad_autonomous_runtime
