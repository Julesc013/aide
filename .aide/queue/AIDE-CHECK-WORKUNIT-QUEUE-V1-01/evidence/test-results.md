# Test Results

Result: `PASS`

Commands:

- `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py core/protocol/workunit.py` -> exit 0
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py` -> 28 tests OK
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py` -> 35 tests OK
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` -> 29 tests OK
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` -> 17 tests OK
- `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` -> 37 tests OK

Unsupported CLI verbs were checked separately and fail closed through argparse
invalid-choice behavior.
