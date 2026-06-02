# Transaction Safety Gates

- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `ce8e207116684b562887dccd8c0c3ebc8bb5726e`
- command: `transaction status`
- mode: report_only
- real_repo_apply_allowed: false
- target_mutation: false
- branch_mutation: false
- worktree_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Required Gates

- repo_identity_confirmed: status=pass; blocks_apply=false
- no_dirty_unrelated_work: status=pass; blocks_apply=false
- file_owned: status=pass; blocks_apply=false
- ownership_boundary_recorded: status=pass; blocks_apply=false
- preimage_hash_recorded: status=pass; blocks_apply=false
- postimage_hash_predicted: status=pass; blocks_apply=false
- staged_diff_reviewed: status=pass; blocks_apply=false
- rollback_record_created: status=pass; blocks_apply=true
- rollback_record_reviewed: status=pass; blocks_apply=true
- conflict_scan_passed: status=pass; blocks_apply=false
- managed_section_markers_valid: status=pass; blocks_apply=false
- secret_scan_passed: status=pass; blocks_apply=false
- no_target_repo_mutation: status=pass; blocks_apply=true
- no_branch_or_worktree_mutation: status=pass; blocks_apply=true
- no_network_provider_github_release: status=pass; blocks_apply=true
- no_real_repo_apply_mode: status=pass; blocks_apply=true
- review_gate_recorded: status=pass; blocks_apply=true

## Boundary

- gates are modeled for future review; AIDE-APPLY-00 does not apply file operations
