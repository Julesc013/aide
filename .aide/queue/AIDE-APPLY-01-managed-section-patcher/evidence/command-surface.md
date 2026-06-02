# Command Surface

## Added Report-Only Commands

- `py -3 .aide/scripts/aide_lite.py managed-section`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py managed-section validate`
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-plan`
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`

## Reports Written

- `.aide/reports/managed-section-status.md`
- `.aide/reports/managed-section-fixture-plan.json`
- `.aide/reports/managed-section-fixture-plan.md`
- `.aide/reports/managed-section-fixture-validation.md`
- `.aide/reports/managed-section-conflict-report.md`
- `.aide/reports/managed-section-next-plan.md`

## Explicit Non-Surface

- No `managed-section apply` subcommand was added.
- No active repository managed-section apply behavior was enabled.
- No install, repair, upgrade, rollback, or uninstall apply behavior was enabled.
- Tests and golden tasks verify `active_repo_managed_section_apply: false`.
