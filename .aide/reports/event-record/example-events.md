# EventRecord Example Events

- status: PASS_WITH_WARNINGS
- task_id: AIDE-BUILD-EVENT-RECORD-SCHEMA-01
- capability_target: minimal_event_record_schema
- example_count: 4
- recorded: false
- projection_only: true

## Examples

- aide://event/EVT-REFERENCE-ID-ACCEPTED: AcceptanceRecorded subject=aide://queue-task/AIDE-ACCEPT-REFERENCE-ID-SCHEME-01
- aide://event/EVT-REFERENCE-ID-PROJECTION: ReferenceIDProjectionRecorded subject=aide://report/reference-id-projection-report
- aide://event/EVT-EVENT-RECORD-PROJECTION: EventRecordProjectionRecorded subject=aide://report/event-record-projection-report
- aide://event/EVT-TESTJOB-ACCEPTED: AcceptanceRecorded subject=aide://queue-task/AIDE-ACCEPT-TESTJOB-SCHEMA-01
