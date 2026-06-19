# Baseline

- task_id: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`
- live_branch: `main`
- live_head_before_repair: `c9ead7df17361ebb980c8000f2995db202270870`
- initial_status: clean worktree, `main...origin/main [ahead 8]`
- canonical_queue: `.aide/queue/index.yaml`
- failed_check: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`
- failed_check_result: `FAILED_VALIDATION`
- failed_check_review_gate: `needs_review`
- failed_check_recommended_next_task: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`
- repair_prompt_source: `.aide/reports/patch-transaction-check/next-task-prompt.md`
- repair_queue_packet_initially_present: `false`
- failed_check_commit_8356599_is_ancestor_of_live_head: `true`
- checked_build_commit_recorded_by_failed_check:
  `2559b1dbc528992451193d942bff741e8cb0a0a7`

The repair was authorized by the live failed-check next-task prompt. Chat
history was not used as queue authority.
