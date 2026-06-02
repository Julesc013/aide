# AIDE-APPLY-00 Prompt

Implement the AIDE transaction model for report-only and fixture-only safe file-operation planning.

Required outputs include transaction schemas, file-operation and managed-section schemas, preimage and postimage records, staged changes, verification records, rollback records, ownership boundaries, conflict records, safety gates, evidence records, policies, examples, documentation, AIDE Lite transaction commands, golden tasks, tests, reports, queue evidence, and next-task packet handoff.

Do not implement real repository apply modes. Do not mutate target repositories. Do not mutate branches or worktrees. Do not publish releases, create tags, upload artifacts, call GitHub APIs, call providers/models/network, run Gateway forwarding, or enable install/repair/upgrade/rollback/uninstall apply behavior.

The task must stop at `needs_review`.
