# Status Consistency

## Queue Index And Status Files

QFIX-01 changed Q09-Q20 from ambiguous `needs_review` to the established
accepted-with-notes convention:

- queue index status: `passed`
- status file status: `passed`
- status file `review_gate.status`: `passed_with_notes`
- `reviewed_at`: `2026-05-07`
- `reviewer`: `Codex`
- `next_allowed_transition`: `superseded_or_reopened_by_future_queue_item`

QFIX-01 itself remains active during implementation and will end as
`needs_review`.

## Q18 Drift Fix

The checkpoint audit found Q18 drift:

- `task.yaml`: `status: running`
- `status.yaml`: `status: needs_review`
- queue index: `status: needs_review`

QFIX-01 reconciled Q18 to:

- `task.yaml`: `status: passed`
- `status.yaml`: `status: passed`
- queue index: `status: passed`
- `task.yaml` result summary: `accepted_with_notes`

This is intentionally a minimal task-status repair, not a scope change.

## Intentional Remaining Nuance

- Q00-Q03 remain `needs_review`; this phase is scoped to Q09-Q20 only.
- Q05 and Q06 still retain earlier raw-status nuance; QFIX-01 does not reopen
  pre-Q09 review history.
- QCHECK remains `needs_review` as a checkpoint audit artifact.
- `.aide/scripts/tests` standard discovery remains expected to fail until
  QFIX-02.
- Generated manifest source fingerprint drift remains reported by Harness and
  is not refreshed in this phase.

## Self-Check Guidance

At baseline, `scripts/aide self-check` still recommended Q09. QFIX-01 updates
the source guidance later in this repair so the post-reconciliation next step is
QFIX-02 rather than stale Q09 work.
