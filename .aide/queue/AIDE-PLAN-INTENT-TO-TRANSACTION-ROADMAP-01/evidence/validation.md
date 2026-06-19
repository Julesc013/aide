# Validation

Validation commands run:

```text
git status --short --branch
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-PLAN-INTENT-TO-TRANSACTION-ROADMAP-01
python JSON parse for .aide/reports/intent-to-transaction-roadmap/roadmap-plan.json
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py doctor
secret-like scan over changed files
```

Results:

- `task inspect`: complete, `missing_evidence: 0`.
- `task evidence`: all 10 declared evidence files present, no missing files.
- `roadmap-plan.json`: parsed successfully.
- `aide_lite.py validate`: `PASS`.
- `aide_lite.py doctor`: `PASS`.
- `git diff --cached --check`: pass; no staged files.
- `git diff --check`: pass with the existing `.aide/queue/index.yaml`
  CRLF-to-LF warning.
- secret-like scan: `PASS` across 28 changed files.

No unrelated generated churn was observed after validation.
