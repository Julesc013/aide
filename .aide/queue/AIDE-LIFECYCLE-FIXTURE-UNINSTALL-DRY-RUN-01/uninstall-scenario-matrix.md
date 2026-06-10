# Uninstall Scenario Matrix

| Scenario | State | Plan | Expected Report | Expected State | Target Class | Check | Residual Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `uninstall-manual-preserved` | PASS_WITH_WARNINGS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/uninstall-manual-preserved.plan.json` | missing | `.aide/examples/apply/lifecycle-fixtures/expected/uninstall-manual-preserved` | fixture | manual file hash matches expected preserved state; generated file deletion remains planned-only | static expected report ref absent |
| `broad-delete-blocked` | PASS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/broad-delete-blocked.plan.json` | `.aide/examples/apply/lifecycle-fixtures/expected-reports/broad-delete-blocked.report.json` | `.aide/examples/apply/lifecycle-fixtures/expected/broad-delete-blocked` | fixture | `BLOCKED_BROAD_DELETE` represented in plan and expected report | blocked scenario metadata only |
