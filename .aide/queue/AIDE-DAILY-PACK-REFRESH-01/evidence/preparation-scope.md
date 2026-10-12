# AIDE Verification Report

## VERIFIER_RESULT

- result: PASS
- method: deterministic repo-local checks
- contents_inline: false
- provider_or_model_calls: none

## CHECK_COUNTS

- info: 10
- warnings: 0
- errors: 0
- checked_files: 0
- changed_files: 10

## CHANGED_FILES

- allowed: `.aide/context/latest-task-packet.md` (M; matches active task allowed path)
- allowed: `.aide/generated/manifest.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/index.yaml` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-command-status.md` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-evidence-bindings.json` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-ledger.md` (M; matches active task allowed path)
- allowed: `DOCUMENTATION.md` (M; matches active task allowed path)
- allowed: `IMPLEMENT.md` (M; matches active task allowed path)
- allowed: `PLANS.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01` (??; matches active task allowed path)

## WARNINGS

- none

## ERRORS

- none

## EVIDENCE_REFS


## LIMITS

- Structural verifier only; no LLM judging.
- Diff scope is path-based only.
- Secret scan is heuristic only.
- Token counts use chars / 4 approximation.
