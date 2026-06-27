# Prompt: AIDE-CHECK-ROLLBACK-BUNDLE-V0-01

Check `AIDE-BUILD-ROLLBACK-BUNDLE-V0-01` as a check-only independent review.

Authority:

- Do not repair implementation.
- Do not accept RollbackBundle v0.
- Do not begin UpdateReceipt, DistributionApplyEngine, self-consumer fixture, canaries, apply behavior, target mutation, release publication, provider/model/network calls, runtime, branch/worktree automation, or promotion.

Required result if the check passes:

- `PASS` or `PASS_WITH_WARNINGS`
- `material_finding_count: 0`
- `missing_evidence: 0`
- recommended next task exactly `AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01`

If material findings are found, recommend exactly `AIDE-BUILD-ROLLBACK-BUNDLE-V0-REPAIR-01` and do not proceed downstream.
