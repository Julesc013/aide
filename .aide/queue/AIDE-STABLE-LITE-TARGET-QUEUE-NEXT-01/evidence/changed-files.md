# Changed files, 2026-09-25

- `.aide/scripts/aide_lite.py`: source-only Task OS phase routing is used only
  for AIDE's explicit self-hosting profile; target profiles override colliding
  source task IDs. Legacy profile-absent fixtures use exact source task IDs.
  Other nonempty queues receive a report-only target queue review action.
  Target next-plan output omits source-only readiness fields.
- `.aide/scripts/tests/test_x_os_01_task_os_commands.py`: prove the one-item
  target queue and colliding-ID cases, retain the zero-item case and source
  phase fixtures.
- `docs/reference/task-os-report-only-commands.md`: state that target next
  work is chosen from target-owned status and evidence.
- This WorkUnit, queue index, `PLANS.md`, and `IMPLEMENT.md`: record narrow
  admission, red/green result, unresolved generator provenance and next gate.

Focused golden tests wrote tracked `.aide/reports/task-os-*` reports containing
this worktree's identity. Those test outputs were restored; no derived export,
release archive, dev ref or target repository was modified by the source task.
