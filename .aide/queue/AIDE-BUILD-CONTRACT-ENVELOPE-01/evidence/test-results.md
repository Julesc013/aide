# Test Results

## Passed

- `py -3 -m py_compile .aide\scripts\aide_lite.py core\protocol\envelope.py`
  - exit code: 0
- `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_contract_envelope.py`
  - exit code: 0
  - result: 19 tests passed
- `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py`
  - exit code: 0
  - result: 17 tests passed
- `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections`
  - exit code: 0
  - result: 37 tests passed

## Coverage Notes

The focused contract-envelope tests cover:

- public envelope shape
- required field validation
- non-object field rejection
- unknown optional field tolerance
- unknown required capability rejection
- SemVer-like compatibility validation
- unknown capability-label rejection
- schema JSON parsing
- lifecycle run and verify projection validity
- source object preservation
- CLI parser dispatch for new and existing lifecycle commands
- CLI status/project/validate success paths
