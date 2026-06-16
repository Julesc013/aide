# Changed Files

## Protocol

- `core/protocol/event_record.py`: EventRecord helper, validation, projection, and report writer.
- `core/protocol/__init__.py`: exports the new protocol module.
- `.aide/protocol/aide-event-record.schema.json`: minimal EventRecord JSON schema.

## CLI And Tests

- `.aide/scripts/aide_lite.py`: adds thin `event-record status/project/validate` dispatch only.
- `.aide/scripts/tests/test_aide_event_record_schema.py`: focused EventRecord schema/helper/projection/CLI tests.

## Reports

- `.aide/reports/event-record/status.md`
- `.aide/reports/event-record/projection-report.json`
- `.aide/reports/event-record/projection-report.md`
- `.aide/reports/event-record/validation.json`
- `.aide/reports/event-record/validation.md`
- `.aide/reports/event-record/event-family-index.json`
- `.aide/reports/event-record/event-family-index.md`
- `.aide/reports/event-record/example-events.json`
- `.aide/reports/event-record/example-events.md`
- `.aide/reports/event-record/future-work.md`
- `.aide/reports/event-record/unfinished-work.md`

## Queue And Logs

- `.aide/queue/AIDE-BUILD-EVENT-RECORD-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
