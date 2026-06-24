# AIDE-BUILD-EUREKA-READONLY-PROCESS-ADAPTER-01 ExecPlan

## Objective

Build a thin Eureka adapter over the unchanged proposed
`RegisteredProcessExecutionProvider v0`.

## Scope

Allowed changes are the Eureka interop adapter, one AIDE Lite command group,
focused tests, task-local evidence, dedicated reports, queue index routing, and
focused root execution logs.

Provider core, neutral protocol files, AIDE self-adapter, Dominium adapter,
Eureka checkout contents, runtime, worker, provider/model/network, preview/apply,
GitHub, branch/worktree, release, and promotion behavior are out of scope.

## Plan

1. Record baseline and command selection.
2. Add `core/interop/eureka/public_alpha_readonly_process_adapter.py`.
3. Add a narrow AIDE Lite command group for status/run/validate.
4. Add focused fake-runner tests for preflight, invocation, decoding, state, and
   evidence hygiene.
5. Run exactly one live Eureka invocation through the adapter when preflight
   passes.
6. Write reports/evidence and stop at `needs_review`.

## Verification

Run focused adapter/provider/AIDE/Dominium tests, adapter validation, broad AIDE
validation, leak scans, diff checks, and commit policy.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, `missing_evidence: 0`, provider
still proposed and unaccepted, and recommended next task exactly
`AIDE-CHECK-EUREKA-READONLY-PROCESS-ADAPTER-01`.
