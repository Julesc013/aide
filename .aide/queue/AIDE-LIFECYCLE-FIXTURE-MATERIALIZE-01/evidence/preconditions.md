# Preconditions

| Check | Result | Evidence | Blocker |
| --- | --- | --- | --- |
| `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` exists | PASS | `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/task.yaml` | none |
| Validator selected this task | PASS | `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/next-batch.md` | none |
| Lifecycle schema validator commands exist and pass | PASS | `lifecycle-schema status`, `validate`, `fixture-verify` passed in preflight | none |
| Lifecycle schemas/examples exist and pass validation | PASS | `lifecycle-schema validate`: PASS, 280 checks | none |
| Fixture plan exists | PASS | `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/fixture-plan.md` | none |
| Scoped transaction executor chain accepted with notes | PASS | `.aide/queue/index.yaml` records `AIDE-CHECK-APPLY-02-RECHECK-01` and `AIDE-APPLY-02-scoped-transaction-executor-v0` as accepted-with-notes planning state | none |
| Repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate`: PASS | none |
| Apply substrate status passes | PASS | `scoped-transaction status`, `managed-section status`, `transaction status`: PASS | none |
| Worktree clean before edits | PASS | `git status --short --branch`: `## main...origin/main` | none |
| Branch ahead state blocks task | PASS | Branch was not ahead at preflight | none |
| Static fixture paths explicitly authorized | PASS | `task.yaml` allowed paths and upstream `next-batch.md` authorize `.aide/examples/apply/lifecycle-fixtures/**` | none |
| Lifecycle apply execution required | PASS | Not required and not performed | none |

Warning: `task next-plan` still selected `AIDE-APPLY-LIFECYCLE-PLAN-01`; the validator task already recorded this Task OS lag, and the validator task-local `next-batch.md` selected `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`.
