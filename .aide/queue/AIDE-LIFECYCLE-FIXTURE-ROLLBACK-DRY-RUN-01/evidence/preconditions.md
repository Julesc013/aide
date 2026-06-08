# Preconditions

| Check | Result | Evidence | Blocker |
| --- | --- | --- | --- |
| `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` exists and selected this task | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/next-batch.md` | None |
| Rollback record checkpoint disposition is `ACCEPTED_WITH_NOTES` | PASS | `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/status.yaml` | None |
| Rollback-compatible record schema exists and was reviewed | PASS | `.aide/apply/lifecycle-rollback-record.schema.json`; prior checkpoint evidence | None |
| Rollback-compatible records exist | PASS | Generic example plus two fixture rollback records | None |
| Generated lifecycle fixture plans link rollback records | PASS | Generated plans for rollback-record-generated, install-managed-section, upgrade-v2 | None |
| Expected reports link rollback records where applicable | PASS | Three expected reports checked | None |
| Fixture metadata exists and parses | PASS | `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`; `.aide/examples/apply/lifecycle-fixtures/scenarios.json` | None |
| Static fixture files referenced by fixture rollback records exist | PASS | Four content refs checked | None |
| Lifecycle schema validator commands exist and pass | PASS | Preflight `lifecycle-schema status`, `validate`, and `fixture-verify` | None |
| AIDE-APPLY-02 accepted-with-notes state exists | PASS | `py -3 .aide/scripts/aide_lite.py task status`; scoped transaction status | None |
| Worktree was clean before this task except no pre-existing task changes | PASS | `git status --short --branch` returned `## main...origin/main` | None |
| Dry-run report output paths are authorized | PASS | This task metadata allows `.aide/reports/lifecycle-fixture-rollback-dry-run/**` | None |
| No rollback execution is required | PASS | Static report-only check model | None |
| No scoped transaction apply against fixture targets is required | PASS | Static report-only check model | None |

Preconditions passed with warnings inherited from the queue: global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, PyYAML remains unavailable so structural fallback is used, and prior expected-report gaps remain outside this task.
