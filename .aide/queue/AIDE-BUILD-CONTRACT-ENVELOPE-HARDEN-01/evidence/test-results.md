# Test Results

Focused checks completed:

| Command | Exit Code | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py` | 0 | PASS | Re-run after fixing an indentation error found by the first attempt. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | 29 tests passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 tests passed; lifecycle temp-runner command output remained scoped to fixture temp workspace. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 tests passed. |

No tests were skipped.
