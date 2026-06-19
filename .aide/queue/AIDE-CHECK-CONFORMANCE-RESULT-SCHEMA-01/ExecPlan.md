# AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` as a bounded,
check-only review gate.

## Scope

- Review the built ConformanceResult schema, helper, CLI, tests, reports, queue
  packet, and evidence without repairing them.
- Recompute profile binding, profile digest, subject binding, case-result
  inventory, aggregation, evidence linkage, record-state separation, admission
  boundary, determinism, source mutation, compatibility, and overclaiming
  checks.
- Write check reports and task-local evidence.
- Update queue index and planning/execution logs.

## Dependencies

- `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` at `needs_review`.
- Checked commit: `2bf53e5`.
- Accepted candidate profile:
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.
- Accepted subject capability:
  `aide://capability/minimal_capability_manifest`.

## Milestones

- Live queue truth verified.
- Build task evidence inspected.
- Independent result/profile/subject/case/aggregation checks run.
- Material findings recorded without repair.
- Check reports and evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run JSON parsing, task inspect/evidence checks, ConformanceResult CLI checks,
predecessor validators, broad AIDE validation, diff checks, and a secret-like
scan. Restore any generated churn outside this check task.

## Exit Criteria

The task stops at `needs_review`, records the independent check result, provides
complete evidence, and recommends either acceptance or a bounded repair task
based on the findings.

## Non-Capabilities

This task does not repair the schema, helper, tests, result projection, case
results, aggregation, profile digest behavior, profile artifacts, subject
artifacts, or predecessor evidence. It does not run cases, create a conformance
runner, collect observations automatically, activate a profile, admit a subject,
grant trust, implement adapters, implement PatchTransaction, implement runtime,
mutate target repositories, mutate GitHub, create branches, push, publish, or
claim production readiness.
