# Validation

## Preflight

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial state was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | Initial HEAD `af6429133767707ae8da4f466e0018202854103f`. |
| `git show --stat --oneline --name-status HEAD -1` | PASS | Previous commit was `audit(protocol): accept stable Reference ID scheme`. |
| `git diff --check` | PASS | No whitespace errors. |
| `git diff --cached --check` | PASS | No staged whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS_WITH_WARNINGS | Task OS still reports stale `latest_task_id: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`; live ReferenceID acceptance records were used instead. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` | PASS | Acceptance task classified complete with no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-REFERENCE-ID-SCHEME-01` | PASS | 15 evidence files available; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py reference-id status` | PASS_WITH_WARNINGS | ReferenceID remains syntactic/projection-only. |
| `py -3 .aide/scripts/aide_lite.py reference-id project --source accepted-protocol` | PASS_WITH_WARNINGS | Source artifacts mutated: false. |
| `py -3 .aide/scripts/aide_lite.py reference-id validate` | PASS_WITH_WARNINGS | Predecessor ReferenceID validation preserved. |
| `py -3 .aide/scripts/aide_lite.py test-job validate` | PASS | Predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py worker-run validate` | PASS | Predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py workunit-queue validate` | PASS | Predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | PASS | Predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | PASS | Predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad repository validation passed; output is very large. |

Preflight generated deterministic report churn outside this task's allowlist in Task OS/TestJob/WorkUnit reports. Because the worktree was clean before preflight, that churn was restored before EventRecord edits.

## EventRecord Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile core/protocol/event_record.py .aide/scripts/aide_lite.py` | PASS | New helper and CLI compile. |
| `py -3 -m json.tool .aide/protocol/aide-event-record.schema.json > $null` | PASS | Schema parses. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_event_record_schema.py` | PASS | 20 tests passed. |
| `py -3 .aide/scripts/aide_lite.py event-record status` | PASS_WITH_WARNINGS | Status report written. |
| `py -3 .aide/scripts/aide_lite.py event-record project --source accepted-reference-id` | PASS_WITH_WARNINGS | Projection report, event family index, and examples written. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | Validation report written; ReferenceID integration preserved. |
| `py -3 .aide/scripts/aide_lite.py event-record status` | PASS_WITH_WARNINGS | Re-run after projection records `projection_report_exists: true`. |

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m json.tool .aide/reports/event-record/projection-report.json > $null` | PASS | Projection report parses. |
| `py -3 -m json.tool .aide/reports/event-record/validation.json > $null` | PASS | Validation report parses. |
| `py -3 -m json.tool .aide/reports/event-record/event-family-index.json > $null` | PASS | Event family index parses. |
| `py -3 -m json.tool .aide/reports/event-record/example-events.json > $null` | PASS | Example events parse. |
| `py -3 .aide/scripts/aide_lite.py reference-id validate` | PASS_WITH_WARNINGS | ReferenceID predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py test-job validate` | PASS | TestJob predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py worker-run validate` | PASS | WorkerRun predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py workunit-queue validate` | PASS | WorkUnit queue predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | PASS | EvidencePacket predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | PASS | ContractEnvelope predecessor validation preserved. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | Task classified complete; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | 16 evidence files available; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad repository validation passed; output is very large. |
| `git diff --check` | PASS_WITH_WARNINGS | Exited 0; Git warned `.aide/queue/index.yaml` will be normalized from CRLF to LF when touched. |
| `git diff --cached --check` | PASS | No staged whitespace errors. |
| `git status --short` | PASS | Only intended EventRecord, queue, report, CLI, test, plan, and implementation-log files remain changed. |

Out-of-scope generated report refreshes from predecessor validators were restored after final validation.
