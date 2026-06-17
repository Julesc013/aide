# Validation

## Result

PASS_WITH_WARNINGS

## Commands Run

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial state was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | Initial HEAD `6a79172ea5806196b4499686f3804fddf4a7e493`. |
| `git show --stat --oneline --name-status HEAD -1` | PASS | Checked EventRecord check commit. |
| `git diff --check` | PASS_WITH_WARNINGS | Final rerun exited 0 after generated report churn was restored; Git warned `.aide/queue/index.yaml` will normalize from CRLF to LF when touched. |
| `git diff --cached --check` | PASS | No staged whitespace errors before edits. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS_WITH_WARNINGS | Latest task packet remains stale; queue truth used. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | Build task classified complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | 16 evidence files available; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EVENT-RECORD-SCHEMA-01` | PASS | Check task classified complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EVENT-RECORD-SCHEMA-01` | PASS | 19 evidence files available; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py event-record status` | PASS_WITH_WARNINGS | Projection-only status retained. |
| `py -3 .aide/scripts/aide_lite.py event-record project --source accepted-reference-id` | PASS_WITH_WARNINGS | Projection generated, source artifacts not mutated. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | ReferenceID integration, predecessor compatibility, and forbidden operation checks passed. |
| `py -3 -m json.tool .aide/reports/event-record/projection-report.json` | PASS | Report parses. |
| `py -3 -m json.tool .aide/reports/event-record/validation.json` | PASS | Report parses. |
| `py -3 -m json.tool .aide/reports/event-record/event-family-index.json` | PASS | Report parses. |
| `py -3 -m json.tool .aide/reports/event-record/example-events.json` | PASS | Report parses. |
| `py -3 -m json.tool .aide/reports/event-record-check/check-report.json` | PASS | Check report parses. |
| `py -3 .aide/scripts/aide_lite.py reference-id validate` | PASS_WITH_WARNINGS | ReferenceID remains syntactic/projection-only. |
| `py -3 .aide/scripts/aide_lite.py test-job validate` | PASS | Passed. |
| `py -3 .aide/scripts/aide_lite.py worker-run validate` | PASS | Passed. |
| `py -3 .aide/scripts/aide_lite.py workunit-queue validate` | PASS | Passed. |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | PASS | Passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | PASS | Passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad repository validation returned `status: PASS`. |
| `py -3 -m json.tool .aide/reports/event-record-accept/acceptance-report.json` | PASS | Acceptance report parses. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01` | PASS | Final rerun classified the task complete with 17 evidence files. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01` | PASS | Final rerun reported 17 evidence files available; missing evidence 0. |

## Generated Churn

Deterministic generated report refreshes outside the acceptance allowlist were restored before acceptance artifacts were written.
