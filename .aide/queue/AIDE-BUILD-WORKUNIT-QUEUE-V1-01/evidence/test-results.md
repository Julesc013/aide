# Test Results

All focused and predecessor tests passed.

- PASS: `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py core/protocol/workunit.py`
- PASS: `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py`
  - exit_code: 0
  - result: 28 tests passed
- PASS: `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py`
  - exit_code: 0
  - result: 35 tests passed
- PASS: `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py`
  - exit_code: 0
  - result: 29 tests passed
- PASS: `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py`
  - exit_code: 0
  - result: 17 tests passed
- PASS: `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections`
  - exit_code: 0
  - result: 37 tests passed
- PASS: `py -3 .aide/scripts/aide_lite.py test`
  - exit_code: 0
  - result: AIDE Lite test status PASS
