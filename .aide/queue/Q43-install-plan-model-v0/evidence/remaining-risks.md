# Remaining Risks

## Q43 Limits

- Q43 has no install apply mode.
- Q43 does not overwrite target files.
- Q43 does not migrate, delete, move, rename, or rewrite files.
- Q43 does not mutate target repos, live branches, GitHub settings, CI workflows, tags, or releases.
- Q43 does not call providers, models, or network services.

## Heuristic Limits

- Install observation and conflict detection are deterministic first-pass heuristics.
- Target repos must generate their own install observations, install plans, ownership ledgers, conflict reports, and dry-run outputs after import.
- Source-generated AIDE install outputs are evidence for this repository only, not target truth.

## Future Dependencies

- Q44 Repair / Doctor Model v0 is needed before repair planning can consume install conflict and preservation evidence.
- Q45/Q46 are still needed for explicit upgrade, rollback, and uninstall models.
- Future apply-capable phases must require review, rollback prerequisites, validation, and target-specific evidence.
