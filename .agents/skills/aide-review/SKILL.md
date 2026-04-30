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

<!-- AIDE-GENERATED:BEGIN section=aide-review-source-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml,.aide/toolchain.lock,.aide/commands/catalog.yaml,.aide/queue/policy.yaml,.aide/queue/index.yaml,docs/reference/source-of-truth.md,docs/reference/harness-v0.md,docs/reference/generated-artifacts-v0.md fingerprint=sha256:5f1663b2b971d30d1569c153bdb13cac8a00c617eaa89ac50058576f216650e1 manual=outside-only -->
## Generated AIDE Source Summary

- Review outcomes are `PASS`, `PASS_WITH_NOTES`, or `REQUEST_CHANGES` unless a task defines a stricter blocker.
- Check scope, evidence, validation, source-of-truth boundaries, generated markers, and review-gate handling.
- Generated downstream artifacts must be deterministic, manifest-backed, and non-canonical.
- Q06 Compatibility, Q07 Dominium Bridge, Runtime, Hosts, and provider work remain out of Q05 review scope.
<!-- AIDE-GENERATED:END section=aide-review-source-summary -->
