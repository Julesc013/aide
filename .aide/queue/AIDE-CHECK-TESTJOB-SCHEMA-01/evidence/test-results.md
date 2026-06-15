# Test Results

Result: PASS.

Commands:

- `py -3 -m py_compile core/protocol/test_job.py`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m json.tool .aide/protocol/aide-test-job.schema.json`: PASS.
- `py -3 -m json.tool .aide/reports/test-job/projection-report.json`: PASS.
- `py -3 -m json.tool .aide/reports/test-job/validation.json`: PASS.
- `json.tool` over `.aide/reports/test-job/projections/*.test-job.json`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_test_job_schema.py`: PASS, 29 tests.
