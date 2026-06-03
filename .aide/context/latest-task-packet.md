# AIDE Latest Task Packet

## PHASE

AIDE-APPLY-02 - Scoped Transaction Executor v0.

## GOAL

Prepare the next bounded apply-substrate phase after AIDE-CHECK-APPLY-01 by defining a scoped transaction executor that can operate only on explicit operator-provided paths and only through validated transaction records.

## WHY

AIDE-APPLY-00 defined the transaction model, and AIDE-APPLY-01 added fixture-safe managed-section planning and verification. AIDE-CHECK-APPLY-01 accepts that patcher with notes and leaves the no-real-apply boundary intact, so the next phase may design a narrowly scoped executor without broad install, repair, upgrade, rollback, uninstall, target, branch, release, provider, model, network, or Gateway behavior.

## CONTEXT_REFS

- `.aide/context/repo-map.json`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/queue/AIDE-APPLY-00-transaction-model/`
- `.aide/queue/AIDE-CHECK-APPLY-00-transaction-model-review/`
- `.aide/queue/AIDE-REVIEW-APPLY-00-transaction-model-review-acceptance/`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/`
- `.aide/queue/AIDE-CHECK-APPLY-01-managed-section-patcher-review/`
- `.aide/reports/managed-section-review.md`
- `.aide/reports/managed-section-apply-boundary.md`
- `.aide/reports/apply-check-01-readiness.md`
- `.aide/reports/aide-apply-02-readiness.md`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`
- `docs/reference/managed-section-patcher.md`
- `docs/reference/managed-section-operations.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-CHECK-APPLY-01-managed-section-patcher-review/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/reports/managed-section-review.md`
- `.aide/reports/managed-section-apply-boundary.md`
- `.aide/reports/managed-section-manual-content-proof.md`
- `.aide/reports/managed-section-conflict-audit.md`
- `.aide/reports/managed-section-rollback-audit.md`
- `.aide/reports/apply-check-01-readiness.md`
- `.aide/reports/aide-apply-02-readiness.md`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/reports/latest-warning-disposition.md`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `.aide/reports/capability-*.md`
- `.aide/reports/capability-*.json`
- `.aide/evals/runs/latest-golden-tasks.*`
- `.aide/verification/latest-verification-report.md`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/generated/manifest.yaml`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.env`
- `.aide.local/**`
- `secrets/**`
- target repositories
- raw provider credentials, API keys, local caches, raw prompt logs, and raw response logs

## IMPLEMENTATION

- Do not implement AIDE-APPLY-02 during AIDE-CHECK-APPLY-01.
- AIDE-CHECK-APPLY-01 may only record review artifacts, validation evidence, warning disposition, and this next-task packet.
- AIDE-APPLY-02 must start from an explicit queue item and ExecPlan before any executor implementation work.

## EVIDENCE

- AIDE-CHECK-APPLY-01 review artifacts under `.aide/queue/AIDE-CHECK-APPLY-01-managed-section-patcher-review/`.
- Top-level checkpoint reports under `.aide/reports/`.
- Latest validation report under `.aide/verification/latest-verification-report.md`.
- Latest golden-task run under `.aide/evals/runs/latest-golden-tasks.*`.

## NON_GOALS

- No install apply.
- No upgrade apply.
- No repair apply.
- No rollback or uninstall apply.
- No target repository mutation.
- No branch/worktree mutation, merge, push, promotion, tag, or release publication.
- No GitHub API mutation.
- No provider/model/network call.
- No Gateway forwarding.
- No broad active-repo patching, delete, move, or rename behavior.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py verify`
- `py -3 .aide/scripts/aide_lite.py managed-section validate`
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`
- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py pack-status`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- AIDE-CHECK-APPLY-01 artifacts exist and status is `needs_review`.
- AIDE-APPLY-01 decision is `ACCEPTED_WITH_NOTES`.
- Managed-section readiness is `READY_FOR_SCOPED_TRANSACTION_EXECUTOR_WITH_WARNINGS`.
- AIDE-APPLY-02 readiness is `READY_FOR_AIDE_APPLY_02_WITH_WARNINGS`.
- No AIDE-APPLY-02 implementation is present in the checkpoint commit.

## OUTPUT_SCHEMA

Return `STATUS`, `SUMMARY`, `VALIDATION`, `WARNINGS`, `RISKS`, and `NEXT`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1203
- budget_status: PASS
