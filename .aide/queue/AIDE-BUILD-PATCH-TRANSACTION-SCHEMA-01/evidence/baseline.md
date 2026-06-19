# Baseline

- live_branch: `main`
- live_head: `ef89d1840dd26480be777b612e4bd443e5a92392` at task start
- baseline_commit_required: `ef89d18`
- baseline_commit_present: true
- initial_worktree_state: clean
- no_fetch_push_reset_merge_rebase: true

Predecessor gates:

- `AIDE-OPERATIONAL-HEALTH-PAUSE-01`: `PASS_WITH_WARNINGS`
- health_pause_readiness: `ready_with_warnings`
- health_pause_recommended_next_task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
- health_pause_task_evidence_missing: `0`
- `AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`: `ACCEPTED_WITH_WARNINGS`

No later PatchTransaction task was present in live queue truth before this task
was materialized.
