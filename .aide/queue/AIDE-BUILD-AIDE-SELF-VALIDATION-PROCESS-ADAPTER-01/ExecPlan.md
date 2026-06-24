# AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01 ExecPlan

## Objective

Build a thin AIDE self-validation adapter that reuses the proposed
`RegisteredProcessExecutionProvider v0` without changing provider core. The
adapter must invoke exactly one allowlisted AIDE Lite validation process for the
successful build proof and stop at `needs_review`.

## Scope

Allowed implementation paths are limited to the AIDE self interop adapter,
one AIDE Lite command wrapper, focused fake-runner tests, this task packet,
task evidence, generated reports, queue index routing, `PLANS.md`, and
`IMPLEMENT.md`.

The task does not accept the registered-process provider, implement a generic
command runner, mutate provider core, add Eureka or Dominium behavior, start a
Service or worker runtime, call providers/models/network, or perform preview,
apply, rollback, GitHub, branch/worktree, release, or promotion behavior.

## Plan

1. Confirm live predecessor check state and missing task surface.
2. Add a domain-thin AIDE adapter over `RegisteredProcessExecutionProvider`.
3. Add report-only `status` and `validate` command surfaces plus one live `run`.
4. Add fake-runner tests for argv, environment, zero-launch refusals, typed
   mappings, deterministic reports, scrubbing, and mutation detection.
5. Materialize queue evidence and reports after exactly one live adapter run.
6. Run focused and broad validation, stop at `needs_review`, and recommend the
   independent check task.

## Verification

Run focused tests, compile checks, adapter report validation, broad AIDE Lite
validation, queue inspection/evidence commands, diff checks, and commit policy.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, `missing_evidence: 0`,
`process_call_count: 1`, `workspace_state_unchanged: true`, provider still
proposed and unaccepted, and recommended next task exactly
`AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.
