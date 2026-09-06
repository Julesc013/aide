# Managed Section Conflict Report

- generated_at: deterministic
- repo_root: `D:/Projects/AIDE/aide`
- current_branch: `task/aide-continuous-worker-pilot-01`
- current_commit: `c39f47ea3cdb2f8359722906f3f486f3c8af19b7`
- command: `managed-section fixture-verify`
- mode: fixture_only
- report_only: true
- fixture_only_patch: true
- real_repo_apply_allowed: false
- active_repo_managed_section_apply: false
- target_mutation: false
- branch_mutation: false
- worktree_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Conflicts

- missing_start_marker: path=.aide/examples/apply/managed-section-fixtures/missing_marker.md; section=aide-fixture-section; apply_blocked=true
- duplicate_start_marker: path=.aide/examples/apply/managed-section-fixtures/duplicate_marker.md; section=aide-fixture-section; apply_blocked=true

## Boundary

- conflicts block managed-section patching
- no active repository files are patched
