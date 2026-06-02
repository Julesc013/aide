# AIDE Latest Task Packet

## PHASE

AIDE-CHECK-APPLY-01 - Managed Section Patcher Review and Apply Boundary Checkpoint.

## GOAL

Review AIDE-APPLY-01 managed-section parser, fixture patcher, conflict detection, rollback-compatible evidence, command surface, docs, golden tasks, export-pack inclusion, and no-real-apply boundary before any later apply-capable phase.

## WHY

AIDE-APPLY-01 implements a fixture-safe managed-section patching primitive. The next step must verify that it preserves manual content, blocks ambiguous markers, remains transaction-compatible, and does not expose active repository apply behavior.

## CONTEXT_REFS

- `.aide/context/repo-map.json`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/task.yaml`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/ExecPlan.md`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/status.yaml`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/evidence/`
- `.aide/reports/managed-section-status.md`
- `.aide/reports/managed-section-fixture-plan.json`
- `.aide/reports/managed-section-fixture-validation.md`
- `.aide/reports/managed-section-conflict-report.md`
- `.aide/reports/managed-section-next-plan.md`
- `core/apply/managed_sections.py`
- `docs/reference/managed-section-patcher.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-CHECK-APPLY-01-*`
- `.aide/queue/AIDE-APPLY-01-managed-section-patcher/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/policies/managed-section*.yaml`
- `.aide/apply/managed-section*.schema.json`
- `.aide/examples/apply/managed-section*`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_apply_01_managed_sections.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/evals/golden-tasks/managed_section_*`
- `.aide/reports/apply-check-01-*.md`
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
- `core/apply/**`
- `docs/reference/managed-section-patcher.md`
- `docs/reference/managed-section-operations.md`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.env`
- `secrets/**`
- `.aide.local/**`
- target repositories
- raw provider credentials, API keys, local caches, raw prompt logs, raw response logs

## IMPLEMENTATION

- Review only; do not implement new apply behavior.
- Inspect AIDE-APPLY-01 code, schemas, reports, tests, golden tasks, docs, evidence, and export-pack inclusion.
- Verify no active repository managed-section apply command exists.
- Verify install, upgrade, repair, rollback, and uninstall apply remain disabled.

## EVIDENCE

- AIDE-APPLY-01 queue packet evidence under `.aide/queue/AIDE-APPLY-01-managed-section-patcher/evidence/`.
- Managed-section status, fixture plan, fixture validation, conflict, and next-plan reports under `.aide/reports/`.
- Full golden-task report under `.aide/evals/runs/latest-golden-tasks.*`.
- Verification and review packets under `.aide/verification/` and `.aide/context/latest-review-packet.md`.

## NON_GOALS

- No active repository managed-section apply.
- No install, upgrade, repair, rollback, or uninstall apply.
- No target repository mutation.
- No branch/worktree mutation, merge, push, promotion, tag, or release publication.
- No GitHub API mutation, provider/model call, network call, or Gateway forwarding.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py managed-section validate`
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`
- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py verify`
- targeted no-real-apply boundary inspection

## ACCEPTANCE

- AIDE-APPLY-01 status is `needs_review`.
- Managed-section parser and fixture patcher are reviewed.
- Manual content preservation and conflict detection evidence is reviewed.
- No-real-apply boundary is preserved.
- Review outcome and next task are recorded.

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `VALIDATION`, `WARNINGS`, `RISKS`, and `NEXT`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 660
- budget_status: PASS
