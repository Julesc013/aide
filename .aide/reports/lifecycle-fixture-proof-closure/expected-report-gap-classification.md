# Expected-Report Gap Classification

Result: `REPAIR_BEFORE_FIXTURE_APPLY_GATE`

## Present Static Expected Reports

- `broad-delete-blocked.report.json`
- `drift-detected.report.json`
- `install-managed-section.report.json`
- `protected-path-blocked.report.json`
- `rollback-record-generated.report.json`
- `traversal-blocked.report.json`
- `upgrade-v2.report.json`

## Missing Static Expected Report Refs

- `install-clean`
- `install-existing-manual-preserved`
- `upgrade-manual-preserved`
- `repair-plan-missing-marker`
- `repair-plan-malformed-marker`
- `uninstall-manual-preserved`

Fixture apply gate planning is deferred until these gaps are repaired or explicitly waived by a later reviewed WorkUnit.
