# QFIX-01 Foundation Review Reconciliation ExecPlan

This is a living execution record for the bounded repair phase
`QFIX-01-foundation-review-reconciliation`.

## Goal

Reconcile source-of-truth state after Q09-Q20 so future agents can trust queue,
profile, command, and self-check guidance without re-auditing already reviewed
token-survival foundation work.

## Scope

- Review Q09-Q20 evidence and classify each as accepted-with-notes, blocked, or
  still-needs-review.
- Align Q09-Q20 queue index and status files with review outcomes.
- Fix Q18 task/status drift.
- Refresh `.aide/profile.yaml`, `.aide/commands/catalog.yaml`, self-check
  next-step guidance, and compact root docs.
- Preserve warnings for substrate-only quality proof, generated manifest drift,
  and `.aide/scripts/tests` discovery failure.

## Non-Goals

- No feature work.
- No Gateway/provider/model/runtime execution.
- No QFIX-02 test-discovery repair.
- No Q21 cross-repo export/import.
- No provider calls, model calls, network calls, secrets, raw prompts, or raw
  responses.

## Validation Intent

Run Harness validation, AIDE Lite validation, Q09-Q20 safety gates, core tests,
the known failing `.aide/scripts/tests` discovery command, diff checks, and a
targeted secret scan. Record every command in task-local evidence.

## Progress

- 2026-05-07: Baseline validation run started from a clean tree at
  `765571932b311f1f9b5310aeee5b2fa7aa55926d`.
- 2026-05-07: Added QFIX-01 queue packet and evidence skeleton.
- 2026-05-07: Reviewed Q09-Q20 and marked each accepted with notes using the
  established `passed` plus `review_gate.status: passed_with_notes` convention.
- 2026-05-07: Fixed Q18 task/status/index drift.
- 2026-05-07: Refreshed profile, command catalog, self-check next-step logic,
  and root docs for the post-token-survival foundation state.
- 2026-05-07: Ran final validation and left QFIX-01 at `needs_review`.
