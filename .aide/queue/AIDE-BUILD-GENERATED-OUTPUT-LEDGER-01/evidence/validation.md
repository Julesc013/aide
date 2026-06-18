# Validation

## Result

`PASS_WITH_WARNINGS`

## Commands

- `py -3 -m core.reconciler.generated_output_ledger`
- `py -3 -m unittest core.reconciler.tests.test_generated_output_ledger`
- `py -3 -m py_compile core/reconciler/generated_output_ledger.py core/reconciler/tests/test_generated_output_ledger.py`
- `validate_generated_output_ledger_reports('.')`
- deterministic rerun hash comparison for ledger and report outputs
- JSON parse for `.aide/ledgers/generated-output.yaml` and report JSON files
- Markdown/JSON finding agreement
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`

## Observed Results

- Focused tests passed: 4 tests.
- Python compile passed.
- Ledger validator returned `validated: true`.
- Deterministic rerun comparison passed.
- No classified source/projection artifact was repaired.
- Unknown provenance/freshness/consumer debt remains explicit.
