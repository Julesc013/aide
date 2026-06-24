# AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01

## Purpose

Build the first bounded `LocalProcessExecutionHost v0` reference slice. The slice
must prove that AIDE can start one allowlisted local reference worker process,
capture a typed result, emit receipt/evidence/event/projection reports, and
preserve the no-mutation and no-provider/no-network boundaries.

## Scope

Allowed implementation paths are limited to:

- `core/execution/local_process_host.py`
- `.aide/fixtures/local-process-execution-host/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_local_process_execution_host.py`
- `.aide/reports/local-process-execution-host/**`
- this task directory, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`

The task must not change the accepted registered-process provider core, the
accepted ExecutionHost contract schema/helper, Dominium/Eureka/AIDE process
adapters, host lanes, Service/runtime, Workbench, provider/model/network, preview,
apply, branch/worktree, GitHub, release, or target-repository surfaces.

## Plan

1. Verify predecessor acceptance and current queue routing.
2. Implement a bounded local process host reference over the accepted registered process provider.
3. Add one committed deterministic reference worker fixture.
4. Add AIDE Lite `local-process-execution-host status/run/validate` commands.
5. Add focused fake-runner tests for exact argv, environment, zero-launch refusals, timeout/malformed/nonzero/schema refusals, mutation detection, determinism, and scrubbing.
6. Generate deterministic reports and task-local evidence.
7. Run validation and stop at `needs_review`.

## Progress

- Completed live repo and predecessor inspection.
- Implemented `core/execution/local_process_host.py`.
- Added `.aide/fixtures/local-process-execution-host/reference_worker.py`.
- Added focused unit tests.
- Added AIDE Lite command surface.
- Generated `.aide/reports/local-process-execution-host/**`.
- Materialized queue packet and evidence.

## Decisions

- The accepted `core/protocol/execution_host.py` contract remains projection-only.
- This build writes a separate reference implementation report instead of widening the accepted contract schema.
- The reference worker is a committed fixture and the only admitted argv shape.
- The provider core remains unchanged; launch still goes through `RegisteredProcessExecutionProvider v0`.

## Validation

Validation commands and results are recorded in `evidence/validation.md`.

## Recovery

If interrupted, rerun:

```bash
py -3 .aide/scripts/aide_lite.py local-process-execution-host run
py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_local_process_execution_host.py
```

The live child process is limited to the committed reference worker fixture and
is safe to rerun; reports are deterministic and overwrite the same output paths.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, `missing_evidence: 0`,
and recommends exactly `AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.
