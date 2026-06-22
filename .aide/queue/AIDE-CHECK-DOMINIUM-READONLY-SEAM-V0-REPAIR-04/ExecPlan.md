# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-04

## Objective

Independently verify that `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-04` at `270b97dc66e477cd37a2f863c8604854a5e90bdf` closes the exact 12 material findings from `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` without reopening earlier safety invariants or widening the offline read-only boundary.

## Scope

This check is limited to task-local independent tools, check reports, queue metadata, and planning/execution logs. Production seam code, schemas, tests, fixtures, generated seam outputs, Repair 04 reports/evidence, historical task records, and Dominium are read-only inputs.

## Non-Goals

Do not repair implementation, accept the seam, create Repair 05, begin acceptance, modify Dominium, invoke Dominium product commands, implement runtime/Workbench/provider/worker behavior, apply patches, mutate repositories, create branches/worktrees, mutate GitHub, release, or promote.

## Allowed Paths

Use the allowlist in `task.yaml`. All production and Repair 04 output surfaces are forbidden final changes; validation commands that refresh generated outputs must be restored before completion.

## Work Packages

1. Baseline: verify clean branch state, predecessor evidence, Repair 03 check result, Repair 04 commit/result/dispositions, and absence of downstream superseding tasks.
2. Independent harness: create task-local tools that avoid importing production validation, conformance, fixture replay, guard builders, portability builders, or Repair 04 disposition logic for material assertions.
3. Twelve-finding closure: independently disposition the exact 12 Repair 04 findings.
4. Regression sampling: sample prior safety invariants, report consistency, explicit non-capabilities, and no capability expansion.
5. Validation: run the requested matrix with timeout handling, restore any out-of-scope generated churn, inspect task evidence, run broad validation, secret-like scan, diff checks, and commit-policy validation.
6. Review gate: stop at `needs_review` with `PASS_WITH_WARNINGS` and `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01` if no material findings remain, otherwise `REQUEST_CHANGES` and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.

## Validation

Run the independent check harness, schema matrix, fixture replay matrix, actual CLI unsupported-operation matrix, no-write state comparison, guard evidence review, operation trace/aggregate recomputation, serialized-manifest portability review, complete output-set comparison, regression sampling, full or split seam test suites, task inspect/evidence, broad `validate`, diff checks, secret-like scan, and commit-policy validation.

## Progress

- 2026-06-22: Baseline verified from live repo: `main` clean before check outputs, Repair 04 commit present, predecessor tasks `missing_evidence: 0`, no downstream check/Repair 05/acceptance task present.
- 2026-06-22: Check-only task packet created and registered.
- 2026-06-22: Independent task-local harness completed full run and recorded `REQUEST_CHANGES` with 4 material findings, 1 warning, and `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05` as the only next recommendation.
- 2026-06-22: Twelve-finding closure matrix recorded exactly 12 dispositions: 9 `CLOSED` and 3 `OPEN`.
- 2026-06-22: Split seam test modules were run after combined unittest discovery timed out. Repair 04, Repair 03, Repair 02, and base modules passed; the first repair module failed one stale next-task routing assertion.
- 2026-06-22: Explicit live `dominium-seam status/snapshot/project/validate/diff/demo` command sequence passed. No out-of-scope generated churn remained in the worktree.

## Decisions

- Repair 04 self-check reports are supporting evidence only and are not used as independent proof.
- Production seam commands may be executed as the system under test, but production helper modules named in the prompt are not imported by the material harness.
- Remaining material defects are not repaired in this task; this check stops at `needs_review`.

## Recovery

If interrupted, inspect `status.yaml`, verify worktree scope, restore out-of-scope generated churn, and continue from the first incomplete work package. Do not repair implementation from this check task.

## Exit Criteria

Stop at `needs_review` only after all 12 findings have independent dispositions, prior sampled invariants remain closed, Dominium remains unchanged, reports/evidence are complete, and exactly one next task is recommended.

Current exit: `needs_review` with `REQUEST_CHANGES`. Exactly one next task is recommended: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`.
