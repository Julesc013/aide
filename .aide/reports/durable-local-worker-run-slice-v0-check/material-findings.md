# Material Findings

## event_record_result_consistency

- category: evidence_truthfulness
- severity: material
- expected: `{"event_payload_result": "PASS"}`
- observed: `{"event_payload_result": null, "event_status_result": "PASS", "fixture_host_result": "PASS"}`
- evidence_refs: .aide/reports/durable-local-worker-run-slice-v0/event-record.json, .aide/reports/durable-local-worker-run-slice-v0/fixture-report.json

EventRecord payload should preserve the observed host result from the durable WorkerRun fixture report.
