# Summary Validation Evidence

Commands:

- `py -3 .aide/scripts/aide_lite.py test summary-validate --file .aide/tests/examples/test-summary.example.json`
- `py -3 .aide/scripts/aide_lite.py test summary-validate --file .aide/tests/examples/test-summary.invalid-raw-log.json`
- `py -3 .aide/scripts/aide_lite.py test slow-report-validate --file .aide/tests/examples/slow-test-report.example.json`

Results:

- Valid compact summary: PASS.
- Invalid raw-log summary: expected FAIL with non-zero exit.
- Slow-test report example: PASS.

The compact test-summary contract rejects raw log payload storage and accepts selected traceback excerpts only.
