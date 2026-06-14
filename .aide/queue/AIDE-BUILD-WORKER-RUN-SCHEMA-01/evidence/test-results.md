# Test Results

## Focused Tests

- `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py core/protocol/workunit.py core/protocol/workunit_cli.py core/protocol/worker_run.py`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_worker_run_schema.py`: PASS, 23 tests

## Related Regression Tests

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli_mutation.py`: PASS, 9 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli.py`: PASS, 10 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py`: PASS, 28 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py`: PASS, 35 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py`: PASS, 29 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py`: PASS, 17 tests
- `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections`: PASS, 37 tests
