# AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01 ExecPlan

## Objective

Independently check `AIDE-DOMINIUM-INTEGRATION-CHARTER-01` without repairing it, modifying Dominium, or implementing any downstream seam/runtime/workbench/provider/mutation work.

## Scope

Allowed writes are limited to:

- `.aide/queue/AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01/**`
- `.aide/reports/dominium-integration-charter-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Plan

1. Verify AIDE branch, clean worktree, source task, predecessor evidence, and absence of superseding downstream tasks.
2. Compare the charter's pinned Dominium snapshot with current remote Dominium `main` using read-only remote/object inspection.
3. Review source-of-truth, semantic ownership, namespace, mapping, command/refusal/diagnostic/evidence/event, transaction, Workbench, compatibility, security, recovery, seam, validation-slice, DAG, and parallel-lane reports.
4. Classify material findings and warnings.
5. Materialize reports and task-local evidence.
6. Run validation, restore unrelated generated churn, commit, and stop at `needs_review`.

## Exit Criteria

The task stops at `needs_review` with exactly one next-task recommendation. It recommends acceptance only if current remote Dominium truth still supports the charter.
