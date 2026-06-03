# Managed Section Status

- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `4f426e7c42106e6e859aafb7a06896e3e7ce9b2a`
- command: `managed-section status`
- mode: report_only
- report_only: true
- fixture_only_patch: false
- real_repo_apply_allowed: false
- active_repo_managed_section_apply: false
- target_mutation: false
- branch_mutation: false
- worktree_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Summary

- policies: true
- schemas: true
- examples: true
- fixtures: true
- core_module: true
- commands: true
- active_repo_apply: false

## Conflict Classes

- missing_start_marker
- missing_end_marker
- duplicate_start_marker
- duplicate_end_marker
- nested_marker
- malformed_marker
- marker_order_invalid
- existing_hash_mismatch
- manual_content_changed
- binary_file
- unsupported_encoding
- destructive_patch
- unknown

## Boundary

- install_apply: false
- upgrade_apply: false
- repair_apply: false
- rollback_uninstall_apply: false
