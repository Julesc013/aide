# Validation

## Commands

- `git diff --check`
  - Result: `PASS`
- `py -3 scripts/aide compile --dry-run`
  - Before refresh: `PASS_WITH_WARNINGS`; manifest would replace.
  - After refresh: `PASS`; manifest would keep.
- `py -3 scripts/aide compile --write`
  - Result: `PASS_WITH_WARNINGS`
  - Reason: write mode refreshed `.aide/generated/manifest.yaml`; generated
    artifacts remain non-canonical.
- `py -3 scripts/aide validate`
  - Result: `PASS`
  - Summary: 149 info, 0 warning, 0 error.
- `py -3 .aide/scripts/aide_lite.py validate`
  - Result: `PASS`
- `py -3 .aide/scripts/aide_lite.py task status`
  - Result: `PASS`
  - Summary: 51 queue items. Q36-Q46, QFIX-04, and QFIX-05 remain
    `needs_review`.
- `py -3 .aide/scripts/aide_lite.py pack-status`
  - Result: `PASS`
  - Details: checksums valid, boundary pass, provenance
    `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py selftest`
  - Result: `PASS`
- `py -3 .aide/scripts/aide_lite.py test`
  - Result: `PASS`
- `py -3 .aide/scripts/aide_lite.py eval run`
  - Result: `PASS`
  - Summary: 117 tasks, 117 pass, 0 warn, 0 fail; no provider/model calls, no
    network calls, no raw prompt storage, no raw response storage.
- `rg -n "sk-[A-Za-z0-9]|sk-ant|api[_-]?key|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|DEEPSEEK_API_KEY" .aide/queue/QFIX-05-release-readiness-warning-reconciliation .aide/generated/manifest.yaml IMPLEMENT.md PLANS.md .aide/queue/index.yaml`
  - Result: `PASS_WITH_FALSE_POSITIVES`
  - Notes: matches were policy/task text such as `token` wording and
    `task-local evidence`, not credentials or private keys.

## Scope Notes

- `.aide/git/**` helper reports were restored after inspection to avoid
  committing stale branch-state generated output.
- `.aide/evals/runs/latest-golden-tasks.*` was restored after `eval run` because
  QFIX-05 records the validation result as evidence without refreshing eval-run
  artifacts outside the task scope.
