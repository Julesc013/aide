# Preconditions

| Check | Result | Evidence |
| --- | --- | --- |
| `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` exists | PASS | task inspect via `--task-id` |
| Upgrade dry-run task status is `needs_review` | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/status.yaml` |
| Upgrade dry-run result is `PASS_WITH_WARNINGS` | PASS | status file and reports |
| Upgrade dry-run selected this checkpoint | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/next-batch.md` |
| Generated upgrade plans exist | PASS | 3 plans parsed |
| Upgrade dry-run reports exist | PASS | `.aide/reports/lifecycle-fixture-upgrade-dry-run/**` parsed |
| Static expected reports exist where referenced | PASS_WITH_WARNINGS | 2 present; `upgrade-manual-preserved` ref absent |
| Fixture scenario metadata parses | PASS | `.aide/examples/apply/lifecycle-fixtures/scenarios.json` |
| Lifecycle schema validator commands pass | PASS | `lifecycle-schema status`, `validate`, `fixture-verify` |
| Full repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate` |
| scoped transaction status passes | PASS | `scoped-transaction status` |
| managed-section status passes | PASS | `managed-section status` |
| transaction status passes | PASS | `transaction status` |
| No dirty worktree blocks checkpoint | PASS_WITH_NOTES | pre-task tree clean; status commands refreshed deterministic reports |

Absent files recorded:

- `.aide/queue/current.toml`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` did not exist before this task
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/validator-plan.md`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-manual-preserved.report.json`
