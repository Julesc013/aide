# Scoped Executor Interlock

Result: `PASS_WITH_NOTES`

Future scoped transaction classes:

- `fixture_dry_run_or_report_only`

Scoped transaction executor v0 limitations preserved:

- no multi-file lifecycle apply execution
- no rollback execution
- no uninstall/delete execution
- no target repo authority

The upgrade dry-run plans set `apply_mode_authorized=false` and remain compatible only with fixture dry-run or report-only planning. This interlock does not block acceptance of the dry-run check, but it does block treating the evidence as upgrade apply, lifecycle apply, fixture apply, active repo apply, target repo apply, production-ready, release-ready, or broad active-repo apply capability.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/scoped-executor-interlock.json`
