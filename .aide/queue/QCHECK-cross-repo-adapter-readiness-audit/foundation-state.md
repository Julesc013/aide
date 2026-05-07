# Foundation State

## Repository Snapshot

- Branch: `main`.
- HEAD: `36dcb5cc9907f0e69d615d99ab2b0a1dcb17a2d0`.
- Worktree at audit start: clean.
- `.aide.local/`: ignored by Git and not tracked.
- Current queue contains QFIX-01, QFIX-02, Q21, Q24, and this checkpoint.
- Q22 and Q23 are not AIDE-source queue items; their evidence exists in the
  sibling target repos.

## QFIX-01

QFIX-01 did reconcile Q09-Q20:

- Q09-Q20 queue index statuses: `passed`.
- Q09-Q20 status file statuses: `passed`.
- Review evidence: `PASS_WITH_NOTES` / `accepted_with_notes`.
- Q18 drift: fixed from running/needs_review mismatch to passed across task,
  status, and index.

QFIX-01 remains `needs_review`, which is appropriate because it was instructed
to stop at review.

## Current Foundation Contradictions

### Profile Drift

`.aide/profile.yaml` is stale:

- `current_focus.summary` still says QFIX-01 completed and QFIX-02 is next
  before Q21.
- `current_focus.queue_item` still points at
  `QFIX-01-foundation-review-reconciliation`.
- `future_intent` still marks QFIX-02 as next and Q21-Q24 as future/planned.

This contradicts:

- `.aide/queue/index.yaml`, which contains Q21 and Q24 as review-state items.
- Q24 evidence, which records post-pilot refresh after Q22/Q23 target evidence.
- Read-only target evidence showing Q22/Q23 pilots are complete and awaiting
  target review.

Severity: P1 state-truth defect. It will waste future agent tokens unless
repaired before further handover work.

### Self-Check Drift

`py -3 scripts/aide self-check` is report-first and passes with warnings, but
its proposed followups still include:

- QFIX-02 before Q21 export/import.
- Cross-repo Q21 only after QFIX-02.
- `next_recommended_step: QFIX-02 review`.

This is no longer current after Q21/Q24 implementation and Q22/Q23 target
pilots. Severity: P1 guidance drift.

### Command Catalog Nuance

`.aide/commands/catalog.yaml` is mostly current and includes:

- AIDE Lite `test` as canonical validation.
- export/import/pack-status commands.
- adapter list/render/preview/validate/drift/generate and adapt.
- Gateway and provider commands labeled report-only/metadata-only.

Remaining nuance: the import-pack note still says real Eureka/Dominium imports
remain Q22/Q23. That was true before target pilots; now target evidence exists.
Severity: P2 documentation/catalog drift.

## Review Gate Posture

- Q00-Q03 remain `needs_review` from early reboot history.
- Q05/Q06 retain raw `needs_review` but have earlier PASS_WITH_NOTES evidence.
- Q07/Q08 are passed with notes.
- Q09-Q20 are passed with notes.
- QFIX-01/QFIX-02/Q21/Q24/QCHECK remain `needs_review`.

This is acceptable only because the queue records review-gate nuance. Future
agents must not treat `needs_review` as equivalent to failed; they must inspect
review evidence.
