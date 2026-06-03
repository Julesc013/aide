# Transaction Fixture Plan

- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `a775b1ac7b9a79c3196841e5475b225f2d676743`
- command: `transaction fixture-plan`
- mode: report_only
- real_repo_apply_allowed: false
- target_mutation: false
- branch_mutation: false
- worktree_mutation: false
- provider_or_model_calls: none
- network_calls: none

## Plan

- transaction_id: transaction-fixture-plan
- mode: fixture_only
- fixture_only_transaction: true
- real_repo_apply_allowed: false

## Operations

- op-create-fixture-file: class=create; path=.aide/examples/apply/fixture-root/generated/fixture-created.txt; fixture_only_allowed=true
- op-managed-section-fixture: class=update_managed_section; path=.aide/examples/apply/fixture-root/AGENTS.fixture.md; fixture_only_allowed=true

## Staged Changes

- stage-create-fixture-file: create -> .aide/examples/apply/fixture-root/generated/fixture-created.txt; verification=pending
- stage-managed-section-fixture: update_managed_section -> .aide/examples/apply/fixture-root/AGENTS.fixture.md; verification=pending

## Rollback Record

- rollback_id: rollback-transaction-fixture-plan
- apply_allowed: false
- rollback_execution: false
