# Preconditions

## Gate Results

| Gate | Result | Evidence |
| --- | --- | --- |
| AIDE-APPLY-02 accepted with notes | PASS | `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml` has `planning_state: accepted_with_notes` and `review_disposition: ACCEPTED_WITH_NOTES`. |
| Recheck accepted repair with notes | PASS | `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/status.yaml` has `recheck_disposition: ACCEPTED_WITH_NOTES`. |
| Historical AIDE-CHECK-APPLY-02 superseded | PASS | `AIDE-QUEUE-CLOSURE-02` and recheck evidence classify the old NEEDS_REPAIR checkpoint as resolved by recheck. |
| AIDE-APPLY-02-REPAIR-01 accepted with notes | PASS | `.aide/queue/AIDE-APPLY-02-REPAIR-01/status.yaml` has `planning_state: accepted_with_notes`. |
| Task OS current/latest reporting repaired | PASS | `AIDE-TASK-OS-STATUS-REPAIR-01` status is `PASS_WITH_WARNINGS`; task inspect reports complete with missing evidence 0. |
| `task next-plan` selects lifecycle planning | PASS | Preflight `task next-plan` selected `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`. |
| Repo validation passes | PASS | Preflight `py -3 .aide/scripts/aide_lite.py validate` returned `status: PASS`. |
| Scoped transaction status passes | PASS | Preflight `scoped-transaction status` returned PASS and reports target/broad/production/release false. |
| Managed-section status passes | PASS | Preflight `managed-section status` returned PASS and report-only boundaries. |
| Transaction status passes | PASS | Preflight `transaction status` returned PASS and real repo apply false. |
| No validation failure blocks planning | PASS | Preflight validation and status commands passed. |
| No stale current-task truth blocks planning | PASS | Task OS status no longer reports raw `AIDE-APPLY-02` as missing. |
| No local dirty worktree blocks planning | PASS_WITH_WARNINGS | Initial worktree was clean; status commands generated report churn that was classified and restored where out of scope. |
| No human review required before planning | PASS | Live Task OS selected this planning WorkUnit; review is required after this plan. |
| Branch ahead state non-blocking | PASS | Preflight branch was `main...origin/main`; after this task commits, local branch is expected to be ahead until pushed by an authorized operation. |

## Gate Conclusion

Lifecycle planning is allowed. Lifecycle apply execution is not authorized.
