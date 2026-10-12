# AIDE Verification Report

## VERIFIER_RESULT

- result: PASS
- method: deterministic repo-local checks
- contents_inline: false
- provider_or_model_calls: none

## CHECK_COUNTS

- info: 9
- warnings: 0
- errors: 0
- checked_files: 0
- changed_files: 9

## CHANGED_FILES

- allowed: `.aide/generated/manifest.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/ExecPlan.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/evidence/validation.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/status.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/index.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/evidence/consumer-effect.md` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/evidence/consumer-job-template.json` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/evidence/consumer-preparation-message.md` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-INSTALLED-BINDING-01/installed_binding.py` (??; matches active task allowed path)

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
