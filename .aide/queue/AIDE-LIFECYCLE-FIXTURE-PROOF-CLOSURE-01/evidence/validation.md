# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git diff --check` - PASS.
- JSON parse of `.aide/reports/lifecycle-fixture-proof-closure/*.json` - PASS; 2 files parsed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01` - PASS; classification complete, 11 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01` - PASS; 11 evidence files listed, none missing.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `rg -n "(_apply_executed|lifecycle_apply_executed|target_mutation|branch_mutation|fixture_apply_authorized|apply_allowed|execution_authorized).*true" ...` - PASS by no matches.

## Warning Classification

- `task next-plan` selector lag is non-blocking for this closure because task-local authority selects `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`.
- Six expected-report gaps are non-blocking for dry-run proof closure but block fixture apply gate readiness until repaired or explicitly waived.
