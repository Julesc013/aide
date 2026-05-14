# Upgrade Dry-Run Report

Latest dry-run artifact: `.aide/upgrade/latest-upgrade-dry-run.json`.

## Summary

- planned updates: 5
- planned skips: 8
- planned preservations: 209
- planned conflicts: 209
- blocking issues: 8
- no apply: true

## Proof

- All operations remain candidate/dry-run only.
- `apply_allowed` is false for all operations.
- `overwrite_allowed` is false for all operations.
- `delete_allowed` is false for all operations.
- `migration_automatic` is false.
- No target mutation is performed by `upgrade dry-run`.

## Blocking Issue Class

The eight blockers are `source_state_leak` records for source-generated or target-state-like files that must not be treated as portable upgrade truth. Q45 plans future review/quarantine/migration only; it performs no action against those paths.
