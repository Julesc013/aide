# AIDE-CHECK-UPDATE-RECEIPT-V0-01 Prompt

Create and process `AIDE-CHECK-UPDATE-RECEIPT-V0-01`.

Repo truth outranks this prompt. Check only. Do not repair implementation, accept UpdateReceipt, start DistributionApplyEngine, mutate target repositories, publish releases, create tags or uploads, call provider/model/network services, automate branches/worktrees, or perform install/update/migration/rollback/repair/uninstall apply.

Objectives:

1. Verify `AIDE-BUILD-UPDATE-RECEIPT-V0-01` exists, is complete, and stopped at `needs_review`.
2. Verify build `missing_evidence` is `0` and material finding count is `0`.
3. Verify UpdateReceipt schema, helper, CLI, fixtures, tests, reports, queue packet, and evidence exist.
4. Verify UpdateReceipt is an update-execution receipt record only and claims no apply, authorization, mutation, release, provider, model, or network capability.
5. Verify predecessor compatibility with DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, and RollbackBundle.
6. Verify required fields, operation receipt classes, skipped-operation reasons, fail-closed semantics, optional extension tolerance, unknown required feature refusal, fixture coverage, path hygiene, and source-output boundaries.
7. Verify no downstream object or external project was started or modified.

Expected result: `PASS`, `PASS_WITH_WARNINGS`, `REQUEST_CHANGES`, `FAILED_VALIDATION`, or `BLOCKED`.

If the result is `PASS` or `PASS_WITH_WARNINGS`, material finding count must be `0`, missing evidence must be `0`, and the next task must be exactly `AIDE-ACCEPT-UPDATE-RECEIPT-V0-01`.

Stop at `needs_review`.
