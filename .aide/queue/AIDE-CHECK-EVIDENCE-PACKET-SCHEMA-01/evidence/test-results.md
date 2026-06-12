# Test Results

Result: `PASS`

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py` | 0 | PASS | compile check |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py` | 0 | PASS | 35 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | 29 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 tests |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 tests |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | broad AIDE Lite test command |

No test failures were observed.
