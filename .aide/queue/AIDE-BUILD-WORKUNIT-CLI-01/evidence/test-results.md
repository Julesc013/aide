# Test Results

All focused and predecessor test commands passed.

| Command | Exit | Result |
| --- | ---: | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py core/protocol/workunit.py core/protocol/workunit_cli.py` | 0 | PASS |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli.py` | 0 | PASS, 10 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py` | 0 | PASS, 28 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py` | 0 | PASS, 35 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS, 29 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS, 17 tests |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS, 37 tests |

Negative command checks:

| Command | Exit | Expected |
| --- | ---: | --- |
| `py -3 .aide/scripts/aide_lite.py workunit create` | 1 | invalid choice, fail closed |
| `py -3 .aide/scripts/aide_lite.py workunit claim` | 1 | invalid choice, fail closed |
| `py -3 .aide/scripts/aide_lite.py workunit run` | 1 | invalid choice, fail closed |
| `py -3 .aide/scripts/aide_lite.py workunit block` | 1 | invalid choice, fail closed |
| `py -3 .aide/scripts/aide_lite.py workunit finish` | 1 | invalid choice, fail closed |
| `py -3 .aide/scripts/aide_lite.py workunit repair` | 1 | invalid choice, fail closed |
