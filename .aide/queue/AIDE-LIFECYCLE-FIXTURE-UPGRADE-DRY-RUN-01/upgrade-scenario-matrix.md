# Upgrade Scenario Matrix

| Scenario | Expected status | Expected blocker | Plan | Expected report | Result |
| --- | --- | --- | --- | --- | --- |
| `upgrade-v2` | `PASS_WITH_WARNINGS` | none | `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-v2.plan.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-v2.report.json` | PASS |
| `upgrade-manual-preserved` | `PASS_WITH_WARNINGS` | none | `.aide/examples/apply/lifecycle-fixtures/generated-plans/upgrade-manual-preserved.plan.json` | absent | PASS_WITH_WARNINGS |
| `drift-detected` | `BLOCKED` | `BLOCKED_DRIFT_DETECTED` | `.aide/examples/apply/lifecycle-fixtures/generated-plans/drift-detected.plan.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/drift-detected.report.json` | PASS |

Machine-readable matrix:

- `.aide/reports/lifecycle-fixture-upgrade-dry-run/upgrade-scenario-matrix.json`
