# Test Results

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide\scripts\aide_lite.py core\apply\lifecycle_fixture_runner.py` | 0 | PASS | No compile errors. |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 focused tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 existing apply tests passed. |

Negative CLI checks:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario does-not-exist --mode apply-temp` | 1 | PASS_EXPECTED_FAIL_CLOSED | Rejected by argparse scenario allowlist before runner execution. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-active` | 1 | PASS_EXPECTED_FAIL_CLOSED | Rejected by argparse mode allowlist before runner execution. |
| `py -3 .aide\scripts\aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode rollback` | 1 | PASS_EXPECTED_FAIL_CLOSED | Rejected by argparse mode allowlist before runner execution. |
