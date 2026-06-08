# Install Scenario Review Evidence

| Scenario | Generated Plan | Generated Report | Static Expected Report | State |
| --- | --- | --- | --- | --- |
| install-clean | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-clean.plan.json` | `.aide/reports/lifecycle-fixture-plans/install-clean.plan-report.json` | absent | PASS_WITH_WARNINGS |
| install-existing-manual-preserved | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-existing-manual-preserved.plan.json` | `.aide/reports/lifecycle-fixture-plans/install-existing-manual-preserved.plan-report.json` | absent | PASS_WITH_WARNINGS |
| install-managed-section | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json` | `.aide/reports/lifecycle-fixture-plans/install-managed-section.plan-report.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json` | PASS |
| protected-path-blocked | `.aide/examples/apply/lifecycle-fixtures/generated-plans/protected-path-blocked.plan.json` | `.aide/reports/lifecycle-fixture-plans/protected-path-blocked.plan-report.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/protected-path-blocked.report.json` | PASS |
| traversal-blocked | `.aide/examples/apply/lifecycle-fixtures/generated-plans/traversal-blocked.plan.json` | `.aide/reports/lifecycle-fixture-plans/traversal-blocked.plan-report.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/traversal-blocked.report.json` | PASS |

The scenario IDs, expected statuses, expected blockers, and mutation-state proof were reviewed independently with JSON parsing.
