# Test Results

Passed:

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

Negative behavior checks also passed by direct helper invocation:

- missing `apiVersion` rejected
- missing `kind` rejected
- non-object `metadata` rejected
- non-object `spec` rejected
- non-object `status` rejected
- unknown optional fields tolerated
- unknown required capability rejected
- invalid SemVer-like compatibility field rejected
- valid SemVer-like compatibility field accepted
- unsupported capability label rejected
- projection source dictionary not mutated
- projection preserves `fixture_temp_apply_only`
- projection preserves explicit non-capabilities
