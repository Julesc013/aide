# AIDE Verification Report

## VERIFIER_RESULT

- result: PASS
- method: deterministic repo-local checks
- contents_inline: false
- provider_or_model_calls: none

## CHECK_COUNTS

- info: 132
- warnings: 0
- errors: 0
- checked_files: 32
- changed_files: 35

## CHANGED_FILES

- allowed: `.aide/commands/catalog.yaml` (M; matches active task allowed path)
- allowed: `.aide/context/context-index.json` (M; matches active task allowed path)
- allowed: `.aide/context/latest-context-packet.md` (M; matches active task allowed path)
- allowed: `.aide/context/latest-task-packet.md` (M; matches active task allowed path)
- allowed: `.aide/context/repo-map.json` (M; matches active task allowed path)
- allowed: `.aide/context/repo-map.md` (M; matches active task allowed path)
- allowed: `.aide/context/repo-snapshot.json` (M; matches active task allowed path)
- allowed: `.aide/context/test-map.json` (M; matches active task allowed path)
- allowed: `.aide/memory/project-state.md` (M; matches active task allowed path)
- allowed: `.aide/prompts/codex-token-mode.md` (M; matches active task allowed path)
- allowed: `.aide/prompts/compact-task.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/ExecPlan.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/evidence/changed-files.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/evidence/remaining-risks.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/evidence/review-packet-savings.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/evidence/review-workflow-report.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/status.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/Q13-evidence-review-workflow/task.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/index.yaml` (M; matches active task allowed path)
- allowed: `.aide/scripts/aide_lite.py` (M; matches active task allowed path)
- allowed: `.aide/verification/latest-verification-report.md` (M; matches active task allowed path)
- allowed: `AGENTS.md` (M; matches active task allowed path)
- allowed: `DOCUMENTATION.md` (M; matches active task allowed path)
- allowed: `IMPLEMENT.md` (M; matches active task allowed path)
- allowed: `PLANS.md` (M; matches active task allowed path)
- allowed: `README.md` (M; matches active task allowed path)
- allowed: `ROADMAP.md` (M; matches active task allowed path)
- allowed: `docs/reference/README.md` (M; matches active task allowed path)
- allowed: `docs/reference/aide-lite.md` (M; matches active task allowed path)
- allowed: `docs/reference/verifier-v0.md` (M; matches active task allowed path)
- allowed: `docs/roadmap/queue-roadmap.md` (M; matches active task allowed path)
- allowed: `docs/roadmap/reboot-roadmap.md` (M; matches active task allowed path)
- allowed: `.aide/context/latest-review-packet.md` (??; matches active task allowed path)
- allowed: `docs/reference/evidence-review-workflow.md` (??; matches active task allowed path)

## WARNINGS

- none

## ERRORS

- none

## EVIDENCE_REFS

- `.aide/context/compiler.yaml`
- `.aide/context/context-index.json`
- `.aide/context/excerpt-policy.yaml`
- `.aide/context/ignore.yaml`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/context/priority.yaml`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/test-map.json`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `.aide/memory/project-state.md`
- `.aide/policies/token-budget.yaml`
- `.aide/policies/verification.yaml`
- `.aide/prompts/codex-token-mode.md`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/scripts/aide_lite.py`
- `.aide/verification/diff-scope-policy.yaml`
- `.aide/verification/evidence-packet.template.md`
- `.aide/verification/file-reference-policy.yaml`
- `.aide/verification/review-decision-policy.yaml`
- `.aide/verification/review-packet.template.md`
- `.aide/verification/secret-scan-policy.yaml`
- `AGENTS.md`
- `DOCUMENTATION.md`
- `IMPLEMENT.md`
- `PLANS.md`
- `README.md`
- `ROADMAP.md`

## LIMITS

- Structural verifier only; no LLM judging.
- Diff scope is path-based only.
- Secret scan is heuristic only.
- Token counts use chars / 4 approximation.
