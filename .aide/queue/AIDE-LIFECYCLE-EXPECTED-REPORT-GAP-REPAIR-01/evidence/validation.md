# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git diff --check` - PASS.
- JSON parse of six new expected reports and repair summary report - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; latest task is `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS with known warning; global selector still chooses `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01` - PASS; classification complete, 9 evidence files, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01` - PASS; 9 evidence files listed, none missing.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` - PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` - PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` - PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS after adding required `EVIDENCE` and `OUTPUT_SCHEMA` sections to the latest task packet.
- `rg -n "(_apply_executed|lifecycle_apply_executed|target_mutation|branch_mutation|fixture_apply_authorized|apply_allowed|execution_authorized).*true" ...` - PASS by no matches.

## Warning Classification

- Generated plan embedded `expected_report_ref` fields remain unchanged by scope.
- `task next-plan` selector lag remains non-blocking for this task because task-local authority selects `AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01`.
- Fixture apply remains unauthorized; the selected next task is a planning gate only.
