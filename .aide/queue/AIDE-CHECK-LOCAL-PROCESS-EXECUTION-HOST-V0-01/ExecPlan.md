# AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01

## Purpose

Independently check `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01` against the
bounded LocalProcessExecutionHost v0 criteria. This is a check-only task and
does not repair implementation.

## Scope

Allowed paths are limited to this check task directory,
`.aide/reports/local-process-execution-host-check/**`, `.aide/queue/index.yaml`,
`PLANS.md`, and `IMPLEMENT.md`.

Forbidden paths include `core/execution/local_process_host.py`,
`core/execution/registered_process.py`, the accepted ExecutionHost contract,
AIDE Lite command implementation, source tests, source fixture, source reports,
and `.aide.local/**`.

## Plan

1. Confirm source baseline and queue routing from live repo state.
2. Inspect source implementation, source task evidence, and generated reports.
3. Run regression commands without repairing implementation.
4. Record independent findings for process boundary, fixture scope, workspace
   containment, events, artifacts, lifecycle, and overclaiming.
5. Materialize check reports and task-local evidence.
6. Stop at `needs_review`.

## Progress

- Confirmed live `main` HEAD and `origin/main` are `e62d5961fa6af6be54e2254ad4006843a169e9c0`.
- Confirmed source task is `needs_review`, `PASS_WITH_WARNINGS`, `missing_evidence: 0`.
- Ran source tests, provider tests, ExecutionHost contract tests, AIDE self-adapter tests, Dominium registered validation backend tests, Eureka process adapter tests, source task inspect/evidence, local host validate, broad AIDE validation, and diff checks.
- Found six material gaps against the requested check boundary.

## Decisions

- Source tests passing is not enough to pass this check because the requested
  acceptance boundary includes disposable workspace containment, event-stream
  validation, artifact integrity, lifecycle transitions, and no-overclaiming
  requirements not proven by the source build.
- The serialized sequence stops at Phase 1 because material findings remain.

## Validation

Validation commands and results are recorded in `evidence/validation-results.md`.

## Recovery

If resumed, rerun:

```bash
py -3 .aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01/evidence/check_local_process_execution_host.py
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```

Do not modify source implementation in this check task.

## Exit Criteria

The task stops at `needs_review` with `REQUEST_CHANGES`, `missing_evidence: 0`,
and recommends exactly `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01`.
