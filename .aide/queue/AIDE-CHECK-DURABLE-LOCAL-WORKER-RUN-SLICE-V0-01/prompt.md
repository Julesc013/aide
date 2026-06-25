# Prompt

Create and process `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.

This is a check-only task. Do not repair implementation.

Independently verify `AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`:

- source-chain consistency and accepted prerequisite use;
- exactly one fixture host process for the valid run;
- authorization before launch and one-use grant consumption;
- durable local Service persistence of WorkUnit, WorkerRun, host outcome,
  EvidencePacket, EventRecord, events, idempotency, and artifact metadata;
- idempotent replay without a second host launch;
- content-addressed artifact integrity and raw event-stream evidence;
- EventRecord and EvidencePacket consistency with independently observed
  behavior;
- unchanged material source state;
- explicit non-capability boundaries remain false;
- committed reports and evidence are scrubbed.

If all material checks pass, recommend exactly:

```text
AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
```

If a material defect remains, recommend exactly:

```text
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01
```
