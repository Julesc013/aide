# Expected-Report Gap Classification Evidence

Static expected reports currently present:

- `broad-delete-blocked.report.json`
- `drift-detected.report.json`
- `install-managed-section.report.json`
- `protected-path-blocked.report.json`
- `rollback-record-generated.report.json`
- `traversal-blocked.report.json`
- `upgrade-v2.report.json`

Missing static expected report refs:

- `install-clean`
- `install-existing-manual-preserved`
- `upgrade-manual-preserved`
- `repair-plan-missing-marker`
- `repair-plan-malformed-marker`
- `uninstall-manual-preserved`

Closure decision: repair these gaps before fixture apply gate planning.
