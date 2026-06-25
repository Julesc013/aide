# AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02 ExecPlan

## Objective

Repair the seven material assertions recorded by
`AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01` while preserving the
already-closed disposable workspace and narrowed descriptor findings.

## Scope

This build may edit only the bounded LocalProcessExecutionHost fixture
implementation, its focused tests, generated local-process reports, this task
packet/evidence, queue index routing, and root execution logs.

It must not modify `RegisteredProcessExecutionProvider v0`, the accepted
ExecutionHost contract, protocol schemas, interop domains, hosts, `.aide.local`,
Workbench, Service, provider/model/network, preview/apply/rollback, branch,
GitHub, release, or promotion surfaces.

## Plan

1. Reproduce the failing Repair 01 check assertions from source reports.
2. Harden path handling with deterministic cross-platform lexical
   classification before filesystem resolution.
3. Correct duplicate-terminal event classification and expand event outcome
   handling for cancelled and reconciliation-required states.
4. Harden artifact declaration and persistence policy with duplicate
   declaration refusal and final access revalidation.
5. Define explicit WorkerRun lifecycle constants, transitions, and cancelled
   terminal support.
6. Expand focused behavioral tests for path, event, artifact, and lifecycle
   matrices.
7. Regenerate local-process reports and write task-local evidence.
8. Run focused and broad validation, then stop at `needs_review`.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, `material_finding_count: 0`,
`missing_evidence: 0`, and next task exactly
`AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02`.
