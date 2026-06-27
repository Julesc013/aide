# Validation Results

Result:

- build result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-CHECK-UPDATE-PLAN-V1-01`

Executed validation:

- `py -3 -m compileall -q core\protocol\update_plan.py .aide\scripts\tests\test_aide_update_plan_v1.py .aide\scripts\aide_lite.py`: `PASS`
- `py -3 -m compileall -q core\protocol .aide\scripts\tests\test_aide_update_plan_v1.py .aide\scripts\aide_lite.py`: `PASS`
- `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_update_plan_v1.py`: `PASS`
- `py -3 .aide\scripts\aide_lite.py update-plan status`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py update-plan project`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py update-plan validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py distribution-manifest validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py project-lock validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger migrate-q43`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py install-record validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py migration-record validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide\scripts\aide_lite.py install validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py repair validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py upgrade validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py rollback validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py uninstall validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py release validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py release draft-validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py validate`: `PASS`
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-UPDATE-PLAN-V1-01`: `PASS`, `missing_evidence: 0`
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-UPDATE-PLAN-V1-01`: `PASS`, no missing evidence
- JSON parse for UpdatePlan schema and reports: `PASS`

Environment gap:

- Direct standalone YAML parse using PyYAML was not available because `yaml` is not installed in this Python environment. Queue/task YAML surfaces were exercised through AIDE task inspect/evidence and broad validation instead.
