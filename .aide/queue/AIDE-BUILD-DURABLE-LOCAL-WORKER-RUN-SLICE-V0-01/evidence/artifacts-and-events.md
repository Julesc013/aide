# Artifacts And Events

The local Service fixture records:

- object records for WorkUnit, WorkerRun, host outcome, EvidencePacket, and EventRecord;
- local Service event sequences `[1, 2, 3, 4, 5, 6]`;
- event types:
  - `trust.authorization_evaluated`
  - `trust.grant_consumed`
  - `durable_worker_run.workunit_recorded`
  - `durable_worker_run.started`
  - `durable_worker_run.completed`
  - `durable_worker_run.evidence_recorded`
- content-addressed artifact metadata for the fixture report and projection.
