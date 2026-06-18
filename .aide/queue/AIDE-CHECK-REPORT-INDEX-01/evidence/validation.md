# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `py -3 -m unittest core.reconciler.tests.test_report_index`
- `py -3 -m py_compile core/reconciler/report_index.py core/reconciler/tests/test_report_index.py`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPORT-INDEX-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPORT-INDEX-01`
- Baseline replay at `bdfa1b7` in a temporary clone.
- JSON/YAML parse and Markdown/JSON agreement checks for check reports.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-REPORT-INDEX-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-REPORT-INDEX-01`

## Observed Results

- Focused tests passed.
- Python compile passed.
- Predecessor task evidence is complete.
- Predecessor baseline counts are reproduced.
- Check reports parse and agree on finding IDs, severity, surface, taxonomy, and next-task routing.
- No inspected report or evidence reference was moved, normalized, repaired, or rewritten.

## Warning

The result is `PASS_WITH_WARNINGS` because predecessor warning findings remain unresolved by design.
