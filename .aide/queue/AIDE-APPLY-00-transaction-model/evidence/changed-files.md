# Changed Files

Task: AIDE-APPLY-00-transaction-model

## Scope Summary

- Added the report-only transaction model under `.aide/apply/`.
- Added transaction policies under `.aide/policies/`.
- Added transaction examples under `.aide/examples/apply/`.
- Added transaction reference docs under `docs/reference/`.
- Added AIDE Lite transaction status, validation, fixture-plan, and fixture-verify report commands.
- Added focused transaction unit tests and six golden tasks.
- Refreshed generated local reports, task status reports, export-pack contents, and golden-task run output.
- Added the queue packet, ExecPlan, prompt, status, and evidence surface for AIDE-APPLY-00.
- Advanced `.aide/context/latest-task-packet.md` to AIDE-APPLY-01 as the next bounded task.

## Directly Added Transaction Sources

- `.aide/apply/README.md`
- `.aide/apply/*.schema.json`
- `.aide/examples/apply/*.example.json`
- `.aide/policies/transactional-apply.yaml`
- `.aide/policies/file-operations.yaml`
- `.aide/policies/transaction-safety-gates.yaml`
- `docs/reference/transaction-model.md`
- `docs/reference/transactional-apply-roadmap.md`
- `docs/reference/managed-section-operations.md`
- `docs/reference/rollback-records.md`
- `.aide/scripts/tests/test_aide_apply_00_transaction_model.py`
- `.aide/evals/golden-tasks/transaction_*_golden/**`

## Generated Or Refreshed Evidence

- `.aide/reports/transaction-model-status.md`
- `.aide/reports/transaction-safety-gates.md`
- `.aide/reports/transaction-fixture-plan.json`
- `.aide/reports/transaction-fixture-plan.md`
- `.aide/reports/transaction-fixture-validation.md`
- `.aide/reports/transaction-next-plan.md`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/evals/runs/latest-golden-tasks.*`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/git/latest-helper-plan.*`
- `.aide/context/latest-review-packet.md`
- `.aide/routing/latest-route-decision.*`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`

## Boundary Notes

- No target repository was mutated.
- No apply-capable command was added.
- No branch, tag, release, GitHub, provider, model, Gateway, or network action was performed.
- `git plan` refreshed helper-plan evidence after report generation made the tree dirty; this was report-only and did not mutate branches.
- `review-pack` and `route explain` refreshed review and advisory routing packets; these were local report-only updates with no provider, model, network, GitHub, branch, or target mutation.
