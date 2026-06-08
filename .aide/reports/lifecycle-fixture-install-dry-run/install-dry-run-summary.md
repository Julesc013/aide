# Lifecycle Fixture Install Dry-Run Summary

- task_id: `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`
- result: `PASS_WITH_WARNINGS`
- report_only: `true`
- dry_run: `true`
- install_scenarios_checked: `5`
- install_apply_implemented: `false`
- install_apply_executed: `false`
- lifecycle_apply_executed: `false`
- scoped_transaction_apply_executed: `false`
- target_files_mutated: `false`
- rollback_execution_implemented: `false`
- target_repo_mutated: `false`
- active_repo_apply_mutation: `false`
- review_gate: `needs_review`

## Scenario Results

| Scenario | Check State | Expected Status | Expected Blocker | Notes |
| --- | --- | --- | --- | --- |
| install-clean | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | static expected report ref absent; generated plan report used as report evidence |
| install-existing-manual-preserved | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | static expected report ref absent; generated plan report used as report evidence |
| install-managed-section | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | none | none |
| protected-path-blocked | PASS | BLOCKED | BLOCKED_PROTECTED_PATH | none |
| traversal-blocked | PASS | BLOCKED | BLOCKED_PATH_TRAVERSAL | none |

## Warnings

- install-clean: static expected report ref absent
- install-existing-manual-preserved: static expected report ref absent

## Defects

- none
