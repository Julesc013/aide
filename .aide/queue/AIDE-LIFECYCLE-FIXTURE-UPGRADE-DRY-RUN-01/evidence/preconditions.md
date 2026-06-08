# Preconditions

| Check | Result | Evidence |
| --- | --- | --- |
| `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` exists and selected this task | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/next-batch.md` |
| Install dry-run checkpoint disposition is `ACCEPTED_WITH_NOTES` | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/status.yaml` |
| Generated plan root exists | PASS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/` |
| Plan index exists and parses | PASS | `plan-index.json` parsed |
| Generated upgrade plan files exist | PASS | 3 upgrade scenario plans parsed |
| Expected upgrade reports exist and parse | PASS_WITH_WARNINGS | 2 static expected reports present; `upgrade-manual-preserved` static expected report ref absent |
| Upgrade scenario metadata exists and parses | PASS | `scenarios.json` parsed |
| Upgrade target baselines exist | PASS | target fixture roots exist |
| Upgrade expected states exist where applicable | PASS | expected-state refs exist |
| Drift-detected scenario expected report exists and parses | PASS | `drift-detected.report.json` parsed |
| Lifecycle schema validator commands pass | PASS | `lifecycle-schema status`, `validate`, `fixture-verify` |
| Lifecycle schemas and examples pass validation | PASS | `lifecycle-schema validate` and repo `validate` |
| AIDE-APPLY-02 accepted-with-notes | PASS | scoped transaction status and accepted-chain status |
| Repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate` |
| scoped-transaction status passes | PASS | `py -3 .aide/scripts/aide_lite.py scoped-transaction status` |
| managed-section status passes | PASS | `py -3 .aide/scripts/aide_lite.py managed-section status` |
| transaction status passes | PASS | `py -3 .aide/scripts/aide_lite.py transaction status` |
| No dirty worktree blocks the task | PASS_WITH_NOTES | pre-task tree clean; status commands refreshed generated reports |
| Dry-run report output paths authorized | PASS | `.aide/reports/lifecycle-fixture-upgrade-dry-run/**` |
| No upgrade apply execution required | PASS | checks are static report-only |
| No scoped transaction fixture apply required | PASS | checks are static report-only |

Absent files recorded:

- `.aide/queue/current.toml`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` did not exist before this task
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-manual-preserved.report.json`
