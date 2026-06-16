# Non-Capability Boundary

Accepted capability:

```text
minimal_reference_id_scheme
```

Accepted behavior:

- `aide://<kind>/<id>` stable identity syntax.
- ReferenceID schema/helper/projection/validation.
- `reference-id status/project/validate` CLI dispatch.
- Deterministic reference-map reports.
- File paths as locators, not identity.
- Optional SHA-256 locator metadata.
- Unknown required ref kinds fail closed.
- Unknown optional ref kinds warn/tolerate where intended.

explicit_non_capabilities:

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

Preservation result:

- Preserved. The acceptance report uses the required field name `explicit_non_capabilities`.
- No alternate field name is used as the primary non-capability field in the acceptance report.
