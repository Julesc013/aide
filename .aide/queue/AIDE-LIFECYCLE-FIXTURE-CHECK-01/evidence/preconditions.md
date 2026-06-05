# Preconditions

| Check | Result | Evidence | Blocker |
| --- | --- | --- | --- |
| Materialization task exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/task.yaml` | none |
| Materialization selected this checkpoint | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/next-batch.md` | none |
| Static fixture root exists | PASS | `.aide/examples/apply/lifecycle-fixtures/` | none |
| Fixture inventory exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/fixture-inventory.md` | none |
| Scenario metadata exists | PASS | `.aide/examples/apply/lifecycle-fixtures/scenarios.json` | none |
| Expected reports exist | PASS | 7 files under `expected-reports/` | none |
| Rollback records exist | PASS | 2 files under `rollback-records/` | none |
| Materialization evidence exists | PASS | 9 evidence files, missing `0` | none |
| Lifecycle-schema commands pass | PASS | status, validate, fixture-verify all PASS | none |
| Scoped transaction accepted-with-notes chain exists | PASS | queue index records `AIDE-CHECK-APPLY-02-RECHECK-01` and `AIDE-APPLY-02` accepted-with-notes planning states | none |
| Repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate`: PASS | none |
| Worktree clean before task | PASS | `git status --short --branch`: `## main...origin/main` | none |
| Branch ahead blocks checkpoint | PASS | final/preflight status did not report ahead | none |
| Checkpoint paths authorized | PASS | queue policy and task-local next batch authorize checkpoint artifacts | none |

Warning: generated `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch selects this checkpoint.
