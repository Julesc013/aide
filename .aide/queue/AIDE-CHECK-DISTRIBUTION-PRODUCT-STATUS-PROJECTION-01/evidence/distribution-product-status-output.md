# Distribution Product Status Output

Captured output from `py -3 .aide/scripts/aide_lite.py distribution-product status` during validation is summarized here.

Key observed lines:

- `result: PASS_WITH_WARNINGS`
- `projection_id: distribution_product_status_v0`
- `next_task: AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `real_target_apply_readiness: false`
- `canary_readiness: false`
- `public_release_readiness: false`
- `package_source_readiness: false`
- `shadow_apply_readiness: false`
- `branch_worktree_apply_readiness: false`
- `provider_model_network_readiness: false`
- `live_runtime_readiness: false`

The command regenerated timestamped projection files; those source projection files were restored afterward because this check task does not authorize changing `.aide/reports/distribution-product-status/current.json` or `current.md`.
