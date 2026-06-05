# Preconditions

| Check | Result | Evidence | Blocker |
| --- | --- | --- | --- |
| Checkpoint exists | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/task.yaml` | none |
| Checkpoint selected this task | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/next-batch.md` | none |
| Checkpoint disposition accepted | PASS | `ACCEPTED_WITH_NOTES` in checkpoint status | none |
| Materialization task complete | PASS | task inspect/evidence show missing `0` | none |
| Static fixture root exists | PASS | `.aide/examples/apply/lifecycle-fixtures/` | none |
| Fixture index parses | PASS | `.aide/examples/apply/lifecycle-fixtures/fixture-index.json` | none |
| Scenario metadata parses | PASS | `.aide/examples/apply/lifecycle-fixtures/scenarios.json` | none |
| Expected reports parse | PASS | 7 expected reports inspected | none |
| Rollback-compatible records parse | PASS | 2 rollback records inspected | none |
| Lifecycle-schema validator passes | PASS | status, validate, fixture-verify commands pass | none |
| AIDE-APPLY-02 accepted chain exists | PASS | task status shows accepted-with-notes planning states | none |
| Repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate`: PASS | none |
| Branch ahead blocks task | PASS | local queue work allowed; branch starts clean | none |
| Plan output paths authorized | PASS | task allowed paths include generated plans and reports | none |
| Lifecycle apply execution required | PASS | not required | none |

Warnings:

- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local sequencing selected this plan-generator task.
- Positional `task inspect/evidence <id>` forms are unsupported; `--task-id` forms passed.
