# Validation

## Preflight

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial state was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push is `https://github.com/Julesc013/aide.git`. |
| `git rev-parse HEAD` | PASS | Initial HEAD `0e686040b18dff32672bc421bbdd95882f9822f0`. |
| `git show --stat --oneline --name-status HEAD -1` | PASS | Checked build commit was `feat(protocol): add EventRecord schema`. |
| `git diff --check` | PASS | No whitespace errors. |
| `git diff --cached --check` | PASS | No staged whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS_WITH_WARNINGS | Task OS latest pointer remains stale; live queue entries were used as authority. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | Build task classified complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EVENT-RECORD-SCHEMA-01` | PASS | 16 evidence files available; missing evidence 0. |

Preflight generated deterministic report churn outside the check output scope in Task OS/TestJob/WorkUnit reports. Those deltas were restored before check artifacts were written.

## EventRecord Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile core/protocol/event_record.py .aide/scripts/aide_lite.py` | PASS | Helper and CLI compile. |
| `py -3 -m json.tool .aide/protocol/aide-event-record.schema.json` | PASS | Schema parses. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_event_record_schema.py` | PASS | 20 tests passed. |
| `py -3 .aide/scripts/aide_lite.py event-record status` | PASS_WITH_WARNINGS | Status report preserved projection-only boundary. |
| `py -3 .aide/scripts/aide_lite.py event-record project --source accepted-reference-id` | PASS_WITH_WARNINGS | Projection report, event family index, and example events were regenerated. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | ReferenceID integration, predecessor compatibility, and forbidden-operation boundaries passed. |

## Predecessor Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py reference-id validate` | PASS_WITH_WARNINGS | ReferenceID predecessor remains projection-only. |
| `py -3 .aide/scripts/aide_lite.py test-job validate` | PASS | TestJob predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py worker-run validate` | PASS | WorkerRun predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py workunit-queue validate` | PASS | WorkUnit queue predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | PASS | EvidencePacket predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py contract-envelope validate` | PASS | ContractEnvelope predecessor validation passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad repository validation passed. |

## Report JSON Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m json.tool .aide/reports/event-record/projection-report.json` | PASS | Build projection report parses. |
| `py -3 -m json.tool .aide/reports/event-record/validation.json` | PASS | Build validation report parses. |
| `py -3 -m json.tool .aide/reports/event-record/event-family-index.json` | PASS | Event family index parses. |
| `py -3 -m json.tool .aide/reports/event-record/example-events.json` | PASS | Example events parse. |
| `py -3 -m json.tool .aide/reports/event-record-check/check-report.json` | PASS | Check report parses. |

## Check Artifact Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EVENT-RECORD-SCHEMA-01` | PASS | Check task classified complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EVENT-RECORD-SCHEMA-01` | PASS | 19 evidence files available; missing evidence 0. |
| `py -3 -m py_compile core/protocol/event_record.py .aide/scripts/aide_lite.py` | PASS | Re-run after check artifacts. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_event_record_schema.py` | PASS | 20 tests passed after check artifacts. |
| `py -3 .aide/scripts/aide_lite.py event-record validate` | PASS_WITH_WARNINGS | Re-run after check artifacts. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad validation returned `status: PASS`. |
| `git diff --check` | PASS_WITH_WARNINGS | Exited 0; Git warned `.aide/queue/index.yaml` will normalize from CRLF to LF when touched. |
| `git diff --cached --check` | PASS | No staged whitespace errors before staging. |

## Final Check Result

`PASS_WITH_WARNINGS`: no blocking defects were found. Warnings are limited to the intended projection-only boundary, minimal JSON Schema subset validation, reserved event family vocabulary, and stale Task OS latest-task packet state.
