# Compatibility Review

Status: PASS.

Compatibility preserved with:

- `minimal_contract_envelope`
- `minimal_evidence_packet_schema`
- `minimal_workunit_queue_v1`
- `minimal_worker_run_schema`

Findings:

- TestJob uses the same `apiVersion/kind/metadata/spec/status` envelope shape.
- TestJob metadata compatibility fields match accepted predecessor patterns.
- TestJob projections include `evidence_packet_refs` as an additive array field.
- TestJob projections can reference WorkUnit task ids through `source_workunit_id`.
- TestJob projections can reference WorkerRun ids when a WorkerRun object is the source; current projected source reports do not require such ids.
- TestJob does not require WorkerRun execution capability.
- TestJob does not require Test Broker runtime capability.
- Projection outputs are additive under `.aide/reports/test-job/` and do not rewrite predecessor projections.

Known limitation: full Draft 2020-12 validation remains deferred consistently with accepted predecessor slices.
