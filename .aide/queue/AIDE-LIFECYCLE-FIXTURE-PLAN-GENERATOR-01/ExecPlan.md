# AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01 ExecPlan

## Purpose

Generate deterministic no-apply lifecycle fixture plan artifacts from the reviewed static fixture repository. This is plan generation only, not apply implementation or apply execution.

## Scope

Allowed writes are limited to this task directory, generated lifecycle fixture plans under `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`, plan-generation reports under `.aide/reports/lifecycle-fixture-plans/**`, queue index/latest packet routing, and deterministic reports refreshed by required validation commands.

No generator CLI command, lifecycle apply implementation, scoped transaction apply against fixture targets, target mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply is authorized.

## Milestones

1. Confirm checkpoint and materialization preconditions.
2. Read fixture index, scenario metadata, expected reports, rollback records, schemas, and examples.
3. Generate one schema-shaped no-apply lifecycle plan for each of the 13 reviewed scenarios.
4. Generate a plan index plus plan-generation and validation reports.
5. Record scoped executor interlock, no-apply proof, capability reality, and remaining risks.
6. Run validation and stop at `needs_review`.

## Validation Intent

Validation must parse all generated JSON plans and reports, confirm 13/13 scenario coverage, confirm required lifecycle plan fields, confirm blocker labels, confirm no-mutation false flags, run AIDE task/lifecycle/schema/apply-substrate status checks, run boundary searches, run a local secret scan, and run commit check after the local commit.

## Review Gate

The final status is `needs_review`. The next safe task is `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`.
