# Baseline

- Source check: `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.
- Source result: `REQUEST_CHANGES`.
- Material finding count: `1`.
- Finding under repair: `event_record_result_consistency`.
- Repair scope: preserve observed host result in durable WorkerRun EventRecord payloads.
