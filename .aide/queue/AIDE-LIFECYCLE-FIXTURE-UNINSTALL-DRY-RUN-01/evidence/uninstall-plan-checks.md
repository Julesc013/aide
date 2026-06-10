# Uninstall Plan Checks

## Result

`PASS_WITH_WARNINGS`

## Findings

- `uninstall-manual-preserved` has a generated uninstall dry-run plan and generated plan report.
- `uninstall-manual-preserved` lacks a static expected report ref but has expected-state evidence.
- `broad-delete-blocked` has a generated uninstall report plan, generated plan report, and static expected report.
- Both plans preserve no-execution flags and target class `fixture`.
