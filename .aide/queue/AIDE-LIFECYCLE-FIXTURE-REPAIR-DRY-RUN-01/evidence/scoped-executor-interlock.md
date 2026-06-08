# Scoped Executor Interlock

Report: `.aide/reports/lifecycle-fixture-repair-dry-run/scoped-executor-interlock.json`

Result: `PASS_WITH_NOTES`

Future scoped transaction classes:

- `fixture_dry_run_or_report_only`
- `managed_section_validation_before_apply`

Blocked scenarios:

- `repair-plan-missing-marker`: blocked by `BLOCKED_MARKER_MISSING`.
- `repair-plan-malformed-marker`: blocked by `BLOCKED_MARKER_MALFORMED`.

Scoped transaction executor v0 limitations preserved:

- no lifecycle repair apply execution
- no multi-file lifecycle apply execution
- no rollback execution
- no uninstall/delete execution
- no target repo authority
- no broad active-repo apply

Interlock blocks acceptance: false

Reason: the repair dry-run is static report-only evidence and does not ask the scoped executor to mutate fixture targets, active repo files, or target repositories.
