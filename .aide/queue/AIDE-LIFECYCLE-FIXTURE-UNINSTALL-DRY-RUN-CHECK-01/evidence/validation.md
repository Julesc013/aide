# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git diff --check` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01` - PASS; classification complete, 10 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01` - PASS; 10 evidence files listed, no missing evidence.
- JSON parse over 8 uninstall dry-run reports in `.aide/reports/lifecycle-fixture-uninstall-dry-run/` - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `rg -n "(_apply_executed|lifecycle_apply_executed|target_mutation|branch_mutation|apply_allowed|execution_authorized).*true" ...` - PASS by no matches.

## Warning Classification

- `task next-plan` selector lag is non-blocking for this checkpoint because task-local authority selects `AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01`.
- `uninstall-manual-preserved` missing static expected report remains non-blocking for uninstall checkpoint acceptance but should be classified in proof closure.
