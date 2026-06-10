# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git diff --check` - PASS.
- JSON parse of `.aide/reports/lifecycle-fixture-apply-gate/gate-decision.json` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01` - PASS; classification complete, 12 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01` - PASS; 12 evidence files listed, none missing.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only; no target, branch, provider/model, or network activity.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only; no active repo apply.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only; target repo capable false, production/release ready false.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `rg -n "(_apply_executed|lifecycle_apply_executed|target_mutation|branch_mutation|fixture_apply_executed|apply_authorized_by_this_gate|apply_allowed|execution_authorized).*true" ...` - PASS by no matches.

## Warning Classification

- The gate selects a future apply WorkUnit but does not authorize apply execution.
- `task next-plan` selector lag remains non-blocking for this task because task-local authority selects `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`.
- Rollback execution remains unimplemented or unauthorized.
- `transaction status` refreshed `.aide/reports/current-aide-roadmap.md`; that out-of-scope generated churn was restored before commit.
