# AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01 ExecPlan

## Objective

Independently recheck `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01` as a
bounded, check-only review gate.

## Scope

- Create the missing repair-check queue task surfaces authorized by the repair
  task's `next-task-prompt.md`.
- Preserve the historical failed check without overwriting or superseding it.
- Recompute the repaired ConformanceResult digest against the pristine accepted
  ConformanceProfile payload using independent `hashlib` and canonical JSON.
- Verify immutability, determinism, incorrect-digest failure behavior, unchanged
  case and aggregation semantics, and preserved non-capability boundaries.
- Write check reports and task-local evidence.

## Dependencies

- Failed check: `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.
- Repair task: `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.
- Checked commit: `00407e4d63d6ad72ce5184bee5b22e07fc56856e`.
- Accepted candidate profile:
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.
- Accepted subject capability:
  `aide://capability/minimal_capability_manifest`.

## Milestones

- Live queue truth verified and missing check task confirmed.
- Repair authorization and predecessor evidence inspected.
- Independent digest and mutation checks run.
- Check reports and evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run Python compile checks, focused ConformanceResult tests, independent digest
recomputation, bad-digest validation, lifecycle-warning copy mutation checks,
repeated projection determinism, ConformanceResult status/project/validate,
JSON report parsing, predecessor validators, task inspect/evidence checks,
broad AIDE validation, diff checks, and a secret-like scan.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, the corrected result
digest equals the independent pristine-profile digest, historical failed-check
evidence remains unchanged, source profile remains unchanged, case and aggregate
semantics remain unchanged, no execution/admission/trust behavior is added, all
check evidence exists, and the next task is
`AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01`.

## Non-Capabilities

This task does not repair the schema, helper, tests, result projection, case
results, aggregation, profile artifacts, subject artifacts, or predecessor
evidence. It does not run cases, create a conformance runner, collect
observations automatically, activate a profile, admit a subject, grant trust,
implement adapters, implement PatchTransaction, implement runtime, mutate target
repositories, mutate GitHub, create branches, push, publish, or claim production
readiness.
