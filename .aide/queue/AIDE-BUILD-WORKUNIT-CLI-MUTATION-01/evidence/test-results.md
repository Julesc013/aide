# Test Results

Recorded command report: `.aide/reports/workunit-cli-mutation/command-results.json`.

Passing tests:

- `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/workunit_cli.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli_mutation.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py`
- `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections`

All expected-zero commands exited 0. Unsupported `claim/run/finish/repair` parser checks exited nonzero as expected.
