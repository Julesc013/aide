# Repair Scenario Matrix Evidence

Matrix file: `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/repair-scenario-matrix.md`

Machine-readable report: `.aide/reports/lifecycle-fixture-repair-dry-run/repair-scenario-matrix.json`

Result: `PASS_WITH_WARNINGS`

| Scenario | State | Plan Path | Expected Report Evidence | Expected Status | Expected Blocker | Path Boundary | Managed-Section Marker | Hash | Mutation State | Residual Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| repair-plan-missing-marker | PASS_WITH_WARNINGS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-missing-marker.plan.json` | expected-state README plus generated plan report | BLOCKED | BLOCKED_MARKER_MISSING | PASS | PASS | PASS | PASS | static expected repair report ref absent |
| repair-plan-malformed-marker | PASS_WITH_WARNINGS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/repair-plan-malformed-marker.plan.json` | expected-state README plus generated plan report | BLOCKED | BLOCKED_MARKER_MALFORMED | PASS | PASS | PASS | PASS | static expected repair report ref absent |

Both scenarios remain report-only and dry-run checked. Neither scenario authorizes lifecycle repair apply, lifecycle apply, scoped transaction fixture apply, active repo mutation, target repo mutation, production-ready status, release-ready status, provider/model calls, Gateway calls, network calls, or broad active-repo apply.
