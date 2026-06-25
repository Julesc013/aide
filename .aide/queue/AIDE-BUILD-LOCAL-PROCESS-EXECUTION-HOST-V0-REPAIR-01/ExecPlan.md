# AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01 ExecPlan

## Objective

Repair only the six material findings from `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

## Scope

Allowed implementation paths are the bounded local process host adapter, its committed reference worker fixture, focused local-host tests, generated local-host reports, this task packet, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

Provider core, the accepted ExecutionHost contract, protocol schemas, interop domains, host adapters, and `.aide.local` Service state remain out of scope.

## Findings To Close

- `local_host.disposable_workspace_not_proven`
- `local_host.path_escape_not_proven`
- `local_host.raw_event_stream_not_proven`
- `local_host.content_addressed_artifacts_not_proven`
- `local_host.workerrun_lifecycle_not_proven`
- `local_host.descriptor_overclaims_operations`

## Implementation Plan

1. Stage the reference worker into a disposable temporary workspace outside the source checkout.
2. Invoke only that staged fixture through `RegisteredProcessExecutionProvider v0` with exact argv and `shell=False`.
3. Replace static JSON worker output with fail-closed NDJSON event stream parsing.
4. Persist the raw event stream and declared worker artifacts under content-addressed report paths.
5. Validate WorkerRun lifecycle transitions from emitted events.
6. Narrow the host descriptor to `probe` and `create_run`, with all other ExecutionHost operations explicitly unsupported.
7. Expand focused tests around the six findings and preserve explicit non-capabilities.
8. Generate repair reports and stop at `needs_review`.

## Verification

Run focused compile checks, local-host tests, one live local reference worker run, local-host validation, broad AIDE validation, diff checks, task inspect/evidence, and commit-policy validation where possible.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, proposed capability `local_process_execution_host_fixture_v0`, and recommends exactly `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`.
