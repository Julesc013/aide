# Next Task Prompt

```text
Create and process AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01.

Repo truth outranks this prompt. Preserve all prior build, failed check, and
repair evidence.

Independently verify that
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01 closes exactly:

event_record_result_consistency

Require the committed durable WorkerRun fixture report host_result and
EventRecord spec.payload.result to match, and verify the focused regression
test exercises build_event_record(report).

Do not repair implementation in this check task.

If the repair passes, recommend exactly:
AIDE-ACCEPT-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01

If a material defect remains, recommend exactly:
AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-02
```
