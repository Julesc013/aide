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

QFIX-01 itself ends as `needs_review` with `review_gate.status:
ready_for_review`.

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
the source guidance so the post-reconciliation next step is QFIX-02 after
QFIX-01 review rather than stale Q09 work.

The refreshed `.aide/runs/self-check/latest.md` is non-canonical report
evidence. It now records:

- Q09-Q20 as accepted/passed-with-notes.
- QFIX-01 as `needs_review`.
- Next recommended step: QFIX-02 AIDE Lite Test Discovery and Runner Fix after
  QFIX-01 review.

## Profile And Catalog Consistency

- `.aide/profile.yaml` no longer points at Q09-era current focus. It records a
  post-token-foundation reconciliation state and keeps live runtime/Gateway/
  provider work deferred.
- `.aide/commands/catalog.yaml` lists `aide self-check` and distinguishes AIDE
  Lite, Gateway, and provider commands as implemented, report-only, or
  metadata-only rather than live execution.
