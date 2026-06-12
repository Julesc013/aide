# Changed Files

Planned changed files for this slice:

- `core/protocol/workunit.py`: minimal WorkUnit queue helper, projection, and validation module.
- `core/protocol/__init__.py`: exports the new protocol module name.
- `.aide/protocol/aide-workunit.schema.json`: minimal WorkUnit queue schema.
- `.aide/scripts/aide_lite.py`: thin `workunit-queue` CLI dispatch.
- `.aide/scripts/tests/test_aide_workunit_queue_v1.py`: focused tests.
- `.aide/reports/workunit-queue/**`: generated status, projection, validation, future-work, unfinished-work, and WorkUnit projection reports.
- `.aide/queue/AIDE-BUILD-WORKUNIT-QUEUE-V1-01/**`: task packet and evidence.
- `.aide/queue/index.yaml`: queue index entry for this task.
