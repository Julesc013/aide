# Distribution Product Status Output

Captured `distribution-product status` validation output included:

- `result: PASS_WITH_WARNINGS`
- `accepted_capabilities: distribution_apply_engine_v0,aide_self_consumer_fixture_v0`
- `accepted_boundaries: distribution_apply_routing_text_repair_v0`
- `next_task: AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `real_target_apply_readiness: false`
- `aide_source_repo_self_apply_readiness: false`
- `canary_readiness: false`
- `public_release_readiness: false`
- `package_source_readiness: false`
- `provider_model_network_readiness: false`
- `branch_worktree_automation_readiness: false`

The command refreshed timestamped projection files during validation. Those source projection files were restored afterward because acceptance does not authorize timestamp-only churn in `.aide/reports/distribution-product-status/current.json` or `current.md`.
