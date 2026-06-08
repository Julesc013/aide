# Managed-Section Checks

Result: `PASS`

Scenarios checked:

- `upgrade-v2`: target and expected files have one managed marker pair; generated content changes from version 1 to version 2 inside the managed section.
- `upgrade-manual-preserved`: target and expected files have one managed marker pair; manual content before and after the managed section is preserved exactly; generated content changes from version 1 to version 2 inside the managed section.
- `drift-detected`: target file has one managed marker pair; scenario is blocked before mutation with `BLOCKED_DRIFT_DETECTED`.

No managed-section patcher was executed. No scoped transaction apply was run.

Detailed machine-readable evidence:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-managed-section-checks.json`
