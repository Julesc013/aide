# AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01 ExecPlan

## Objective

Close the single material finding from the durable local WorkerRun check:
`event_record_result_consistency`.

## Scope

The repair is limited to EventRecord result preservation, a focused regression
test, regenerated durable WorkerRun reports, repair reports, task-local
evidence, queue index, and root plan/log updates.

## Method

- Preserve the observed host result when building EventRecord payloads from
  either live host results or normalized fixture reports.
- Add a regression assertion that `build_event_record(report)` preserves
  `PASS`.
- Regenerate durable WorkerRun reports.
- Produce repair evidence and route to an independent repair check.

## Stop Condition

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`.
