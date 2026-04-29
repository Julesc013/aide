---
name: aide-review
description: Review completed AIDE queue items for scope, evidence, validation, policy compliance, and review-gate handling.
---

## Use When

- A queue item reaches `needs_review`.
- A human asks for review of a completed or blocked queue task.
- Evidence must be checked against acceptance criteria.

## Review Checklist

- Compare changed files against allowed and forbidden paths.
- Read task evidence and confirm validation commands were run.
- Check that blockers, deferrals, and review gates are explicit.
- Confirm no unsupported compatibility, support, capability, release, or parity claims were added.
- Verify generated outputs are deterministic and reviewable where applicable.
- Confirm `status.yaml` matches the reviewed outcome.

## Outcomes

- `PASS`: acceptance criteria and validation are satisfied.
- `PASS_WITH_NOTES`: acceptable, with documented limitations or follow-up work.
- `REQUEST_CHANGES`: scope, evidence, validation, or policy issues must be fixed before passing.

