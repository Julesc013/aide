# Test Results

| Command | Exit Code | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py` | 0 | PASS | Syntax check passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | 29 tests passed. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 tests passed. |
| direct negative/alignment checks | 0 | PASS | 29 checks, zero failures. |
