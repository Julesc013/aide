# Rollback Dry-Run Report

Command: `py -3 .aide/scripts/aide_lite.py rollback dry-run`

- Result: PASS.
- Dry-run path: `.aide/rollback/latest-rollback-dry-run.json`.
- Operations: 229.
- Planned future restores: 1.
- Planned future removals: 4.
- Planned preservations: 224.
- Blockers: 0.
- `no_apply`: true.
- `target_mutation`: false.
- `overwrite`: false.
- `delete`: false.
- Managed-section removal: false by operation gate.

The dry-run uses future-action language only. It did not restore previous files,
remove new files, overwrite files, delete files, mutate target state, or remove
managed sections.
