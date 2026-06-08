# Preconditions

| Check | Result | Evidence |
| --- | --- | --- |
| Generator task exists and selected this checkpoint | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/next-batch.md` |
| Generated plan root exists | PASS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/` |
| Plan index parses | PASS | `plan-index.json` parsed by local JSON review |
| 13 generated plan files exist | PASS | 13 `*.plan.json` files found |
| Generated plan reports exist | PASS | 13 `*.plan-report.json` files found |
| Generator evidence exists | PASS | `task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` reported 9 files, missing 0 |
| Fixture checkpoint accepted materialization with notes | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/status.yaml` |
| Static fixture root exists | PASS | `.aide/examples/apply/lifecycle-fixtures/` |
| Scenario metadata parses | PASS | `scenarios.json` parsed by local JSON review |
| Expected reports exist and parse | PASS | 7 expected report JSON files reviewed |
| Rollback-compatible records exist and parse | PASS | 2 rollback JSON files reviewed |
| Lifecycle schema validator commands pass | PASS | `lifecycle-schema status`, `validate`, and `fixture-verify` |
| AIDE-APPLY-02 accepted-with-notes | PASS | `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml` |
| Repo validation passes | PASS | `py -3 .aide/scripts/aide_lite.py validate` |
| scoped-transaction status passes | PASS | `py -3 .aide/scripts/aide_lite.py scoped-transaction status` |
| managed-section status passes | PASS | `py -3 .aide/scripts/aide_lite.py managed-section status` |
| transaction status passes | PASS | `py -3 .aide/scripts/aide_lite.py transaction status` |
| No dirty worktree blocker | PASS_WITH_NOTES | Preflight dirtiness was deterministic report refresh after status commands |

Absent files recorded:

- `.aide/queue/current.toml`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/validator-plan.md`
