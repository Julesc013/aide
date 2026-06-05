# Fixture Review

## Inventory

- Fixture root: `.aide/examples/apply/lifecycle-fixtures/`
- Source pack: present.
- Target baselines: present.
- Expected states: present.
- Scenario metadata: present.
- Fixture index: present.
- Expected reports: 7 present.
- Rollback-compatible records: 2 present.

## Scenario Coverage

All 13 planned scenarios are present:

1. `install-clean`
2. `install-existing-manual-preserved`
3. `install-managed-section`
4. `upgrade-v2`
5. `upgrade-manual-preserved`
6. `drift-detected`
7. `repair-plan-missing-marker`
8. `repair-plan-malformed-marker`
9. `rollback-record-generated`
10. `uninstall-manual-preserved`
11. `protected-path-blocked`
12. `traversal-blocked`
13. `broad-delete-blocked`

## Result

PASS_WITH_NOTES. Static fixture materialization is complete enough for future dry-run/report-only plan generation.
