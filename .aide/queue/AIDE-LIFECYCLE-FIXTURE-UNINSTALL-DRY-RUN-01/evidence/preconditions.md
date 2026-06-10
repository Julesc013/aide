# Preconditions

| Precondition | Result | Evidence |
| --- | --- | --- |
| Rollback dry-run checkpoint exists and is accepted with notes | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/status.yaml` |
| Uninstall scenarios exist in fixture metadata | PASS | `uninstall-manual-preserved`, `broad-delete-blocked` |
| Generated uninstall plans exist | PASS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/*.plan.json` |
| Generated plan reports exist | PASS | `.aide/reports/lifecycle-fixture-plans/*.plan-report.json` |
| Expected report evidence exists where claimed | PASS_WITH_WARNINGS | `broad-delete-blocked` has a static expected report; `uninstall-manual-preserved` lacks one. |
| No uninstall execution is required | PASS | Plans and reports are report-only/dry-run. |

## Result

Preconditions passed with a non-blocking expected-report gap for `uninstall-manual-preserved`.
