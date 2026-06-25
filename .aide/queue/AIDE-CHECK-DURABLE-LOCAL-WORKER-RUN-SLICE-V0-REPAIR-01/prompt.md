# AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01

Create and process `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`.

This is a check-only task. Repository truth and `.aide/queue/index.yaml`
outrank handoff documents and generated roadmap prose.

Independently verify that
`AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01` closes the exact
material finding from `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`:

```text
event_record_result_consistency
```

Require:

- the source check recorded exactly one material finding;
- Repair 01 reports `PASS_WITH_WARNINGS`, `material_finding_count: 0`, and
  `missing_evidence: 0`;
- `.aide/reports/durable-local-worker-run-slice-v0/fixture-report.json`
  records `host_result: PASS`;
- `.aide/reports/durable-local-worker-run-slice-v0/event-record.json`
  records `spec.payload.result: PASS` and `status.result: PASS`;
- source and focused test coverage demonstrate the normalized `host_result`
  case is covered;
- false-boundary fields remain false;
- source/workspace unchanged claims remain true;
- reports and evidence are scrubbed;
- no production code is modified by this check.

If the check passes, recommend exactly:

```text
AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
```

If material findings remain, recommend exactly:

```text
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-02
```

Stop at `needs_review`.
