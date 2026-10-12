# AIDE Verification Report

## VERIFIER_RESULT

- result: PASS
- method: deterministic repo-local checks
- contents_inline: false
- provider_or_model_calls: none

## CHECK_COUNTS

- info: 17
- warnings: 0
- errors: 0
- checked_files: 0
- changed_files: 17

## CHANGED_FILES

- allowed: `.aide/context/latest-task-packet.md` (M; matches active task allowed path)
- allowed: `.aide/generated/manifest.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/ExecPlan.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/run_checks.py` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/status.yaml` (M; matches active task allowed path)
- allowed: `.aide/queue/index.yaml` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-command-status.md` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-evidence-bindings.json` (M; matches active task allowed path)
- allowed: `.aide/reports/capability-ledger.md` (M; matches active task allowed path)
- allowed: `.aide/scripts/aide_lite.py` (M; matches active task allowed path)
- allowed: `.aide/scripts/tests/test_task_binding.py` (M; matches active task allowed path)
- allowed: `DOCUMENTATION.md` (M; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/evidence/baseline-failures.json` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/evidence/baseline-manifest.json` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/evidence/source-message.md` (??; matches active task allowed path)
- allowed: `.aide/queue/AIDE-DAILY-TASK-BINDING-01/evidence/source-structural-observation.json` (??; matches active task allowed path)
- allowed: `docs/reference/task-packets.md` (??; matches active task allowed path)

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
