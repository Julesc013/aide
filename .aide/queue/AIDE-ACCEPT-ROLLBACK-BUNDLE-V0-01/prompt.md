# Prompt: AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01

Create and process `AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01`.

Repo truth outranks this prompt. Confirm the live checkout, queue index, build task, check task, evidence, and reports before acting.

## Authority

Acceptance only.

Do not modify RollbackBundle implementation, repair defects, start UpdateReceipt, start DistributionApplyEngine, perform rollback apply, perform install/update/migration/uninstall apply, mutate target repositories, create release archives/tags/uploads/GitHub Releases, call provider/model/network services, touch ScreenSave/Eureka/Dominium, or automate branches/worktrees.

## Acceptance Objectives

1. Confirm `AIDE-BUILD-ROLLBACK-BUNDLE-V0-01` exists, is complete, and stopped at `needs_review`.
2. Confirm `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01` exists, is complete, and stopped at `needs_review`.
3. Confirm the latest independent check result is `PASS` or `PASS_WITH_WARNINGS`.
4. Confirm `material_finding_count: 0`.
5. Confirm `missing_evidence: 0`.
6. Confirm no RollbackBundle implementation files were changed by the check.
7. Accept only RollbackBundle v0 as a no-apply rollback-preparation contract.
8. Record accepted predecessor dependencies, modeled fields, reverse operation classes, limitation model, fail-closed semantics, warnings, explicit non-capabilities, and downstream-use boundary.
9. Recommend exactly one next task: `AIDE-BUILD-UPDATE-RECEIPT-V0-01`.

## Expected Result

`ACCEPTED_WITH_WARNINGS`

Stop at `needs_review`.
