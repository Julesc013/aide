# Test Results

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile .aide\scripts\aide_lite.py core\apply\lifecycle_fixture_runner.py` | PASS | CLI and runner module compile. |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 17 focused tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 existing apply tests passed. |

New focused coverage:

- unsupported operation and malformed plan rejection
- overclaiming report fail-closed behavior
- malformed rollback record fail-closed behavior
- missing required run field fail-closed behavior
- empty and wildcard path-jail rejection
- missing managed-section marker failure
