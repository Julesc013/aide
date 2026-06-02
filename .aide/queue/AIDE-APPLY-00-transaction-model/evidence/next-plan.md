# Next Plan

Task: AIDE-APPLY-00-transaction-model

## Current Result

AIDE-APPLY-00 is complete enough for review and is marked `needs_review`.

## Next Queue Item

Next bounded task: AIDE-APPLY-01-managed-section-patcher

## Planned Scope For AIDE-APPLY-01

- Build a managed-section patcher around the transaction model.
- Keep writes fixture-only or review-gated unless a future policy explicitly authorizes apply behavior.
- Reuse the transaction schemas and safety gates introduced in AIDE-APPLY-00.
- Preserve no target mutation, no branch mutation, no release/GitHub/provider/network behavior unless separately authorized.

## Review Gate

AIDE-APPLY-00 must be reviewed before treating the transaction model as accepted repository policy.
