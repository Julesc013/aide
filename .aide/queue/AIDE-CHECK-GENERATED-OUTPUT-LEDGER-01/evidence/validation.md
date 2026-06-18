# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `py -3 -m unittest core.reconciler.tests.test_generated_output_ledger`
- `py -3 -m py_compile core/reconciler/generated_output_ledger.py core/reconciler/tests/test_generated_output_ledger.py`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
- Baseline replay at `af3156a` in a temporary clone.
- JSON/YAML parse and Markdown/JSON agreement checks for check reports.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`

## Observed Results

- Focused tests passed.
- Python compile passed.
- Predecessor task evidence is complete.
- Predecessor baseline counts are reproduced.
- Check reports parse and agree on finding IDs, severity, surface, taxonomy, and next-task routing.
- No predecessor ledger or report output was rewritten.

## Warning

The result is `PASS_WITH_WARNINGS` because predecessor warning findings remain unresolved by design.
