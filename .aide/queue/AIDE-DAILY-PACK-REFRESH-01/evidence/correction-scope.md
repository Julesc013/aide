# AIDE Verification Report

## VERIFIER_RESULT

- result: PASS
- method: deterministic repo-local checks
- contents_inline: false
- provider_or_model_calls: none

## CHECK_COUNTS

- info: 6
- warnings: 0
- errors: 0
- checked_files: 0
- changed_files: 6

## CHANGED_FILES

- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/ExecPlan.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/evidence/preparation-checks.json` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/evidence/refresh-job-template.json` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/evidence/correction-message.md` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/evidence/review-00f1f428.json` (??; matches active task allowed path)

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
