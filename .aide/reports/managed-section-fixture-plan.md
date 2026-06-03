# Managed Section Fixture Plan

- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `e1bbccebbe7f1d3c5e2d4e8b6c9f03bf73d349c6`
- command: `managed-section fixture-plan`
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

## Plan

- report_id: managed-section-fixture-plan
- status: PASS
- fixture_only_patch: true
- active_repo_managed_section_apply: false

## Sections

- aide-fixture-section: path=.aide/examples/apply/managed-section-fixtures/valid_input.md; manual_content_preserved=true

## Conflicts

- missing_start_marker: path=.aide/examples/apply/managed-section-fixtures/missing_marker.md; blocked=true
- duplicate_start_marker: path=.aide/examples/apply/managed-section-fixtures/duplicate_marker.md; blocked=true

## Rollback Evidence

- rollback_id: rollback-aide-fixture-section
- rollback_execution: false
- real_repo_apply_allowed: false
