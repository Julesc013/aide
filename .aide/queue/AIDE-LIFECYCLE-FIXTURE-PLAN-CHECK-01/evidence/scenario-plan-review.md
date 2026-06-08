# Scenario Plan Review Evidence

Scenario coverage:

- PASS_WITH_WARNINGS: `install-clean`, `install-existing-manual-preserved`, `install-managed-section`, `upgrade-v2`, `upgrade-manual-preserved`, `rollback-record-generated`, `uninstall-manual-preserved`.
- BLOCKED: `drift-detected`, `repair-plan-missing-marker`, `repair-plan-malformed-marker`, `protected-path-blocked`, `traversal-blocked`, `broad-delete-blocked`.

Blocked labels:

- `drift-detected`: `BLOCKED_DRIFT_DETECTED`
- `repair-plan-missing-marker`: `BLOCKED_MARKER_MISSING`
- `repair-plan-malformed-marker`: `BLOCKED_MARKER_MALFORMED`
- `protected-path-blocked`: `BLOCKED_PROTECTED_PATH`
- `traversal-blocked`: `BLOCKED_PATH_TRAVERSAL`
- `broad-delete-blocked`: `BLOCKED_BROAD_DELETE`

Modes and mutation states:

- Dry-run mode: 6 scenarios.
- Report mode: 7 scenarios.
- `static_fixture_only`: 6 scenarios.
- `blocked_no_mutation`: 6 scenarios.
- `static_record_only`: 1 scenario.
