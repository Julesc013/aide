# Non-Capability Boundary

Accepted capability: `minimal_reconciler_reports`

Accepted behavior:

- report-only Reconciler helper
- reconciler status/report/validate CLI dispatch
- finding taxonomy
- deterministic findings report
- queue/protocol/evidence/report/ReferenceID/EventRecord/OKF drift checks
- stale latest-task-packet detection/classification
- acceptance gate debt detection/classification
- missing evidence/report ref checks
- OKF/protocol/report mismatch checks
- capability overclaim checks
- ReferenceID/EventRecord report consumption where practical
- advisory findings with mutation performed false
- explicit no-repair/no-mutation boundary

Field: `explicit_non_capabilities`

- reconciler_repair
- reconciler_mutation
- auto_fix
- auto_acceptance
- auto_supersede
- auto_latest_task_update
- okf_auto_update
- protocol_report_auto_update
- scheduler
- leases
- supervisor
- runtime
- service
- commander
- capability_manifest
- conformance_profile
- patch_transaction
- adapter_manifest
- context_pack_v2
- event_sourcing_runtime
- append_only_runtime_store
- runtime_event_log
- state_reconstruction
- test_broker_runtime
- async_execution
- worker_execution
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
- production_readiness
- release_readiness
- broad_autonomous_runtime
