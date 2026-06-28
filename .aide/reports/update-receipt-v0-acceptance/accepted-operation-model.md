# Accepted Operation Model

Accepted operation receipt classes:

- `managed_file_added`
- `managed_file_updated`
- `managed_file_removed`
- `managed_section_added`
- `managed_section_updated`
- `managed_section_removed`
- `project_owned_preserved`
- `project_overlay_preserved`
- `local_only_preserved`
- `runtime_generated_preserved`
- `evidence_only_preserved`
- `legacy_preserved`
- `never_touch_preserved`
- `migration_recorded`
- `lock_updated`
- `ownership_ledger_updated`
- `install_record_updated`
- `validation_run`
- `validation_skipped`
- `manual_review_recorded`
- `operation_refused`
- `operation_failed`
- `rollback_bundle_referenced`

Receipt classes are records of observed or future fixture execution facts, not commands.
