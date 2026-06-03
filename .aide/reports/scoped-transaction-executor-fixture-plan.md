# Scoped Transaction Executor Fixture Plan

- generated_at: deterministic
- repo_root: `C:/Projects/AIDE/aide`
- current_branch: `main`
- current_commit: `e1bbccebbe7f1d3c5e2d4e8b6c9f03bf73d349c6`
- command: `scoped-transaction fixture-plan`
- mode: dry-run
- scoped_transaction_executor: true
- review_gate: needs_review
- production_ready: false
- release_ready: false
- target_repo_mutation: false
- branch_mutation: false
- worktree_mutation: false
- provider_or_model_calls: none
- Gateway calls: none
- network_calls: none
- broad_active_repo_apply: false

## Plan

- transaction_id: scoped-transaction-executor-fixture
- mode: dry-run
- dry-run target mutation: false

## Operations

- op-scoped-managed-section-fixture: type=update_managed_section; path=.aide/examples/apply/scoped-transaction-executor-fixtures/valid_input.md; preimage hash required=true; postimage verification=true

## Records

- report_path: .aide/reports/scoped-transaction-executor-fixture-report.json
- rollback_record_path: .aide/reports/scoped-transaction-executor-fixture-rollback.json
- staged-change record expected: true
- rollback-compatible record expected: true
