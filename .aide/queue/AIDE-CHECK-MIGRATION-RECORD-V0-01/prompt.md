# Prompt: AIDE-CHECK-MIGRATION-RECORD-V0-01

Create and process `AIDE-CHECK-MIGRATION-RECORD-V0-01`.

Authority:

- Check only.
- Do not repair implementation.
- Do not accept MigrationRecord v0.
- If material findings exist, recommend a bounded repair task.

Result:

- `REQUEST_CHANGES`
- finding: `migration_record.fixture_report_absolute_paths`
- next task: `AIDE-BUILD-MIGRATION-RECORD-V0-REPAIR-01`
