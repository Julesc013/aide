# Test Results

Result: `PASS`

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | 0 | PASS | compile check |
| `py -3 -m py_compile core/protocol/envelope.py` | 0 | PASS | compile check |
| `py -3 -m py_compile core/protocol/evidence_packet.py` | 0 | PASS | compile check |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py` | 0 | PASS | focused EvidencePacket tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | contract-envelope compatibility tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | lifecycle compatibility tests |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | apply core tests |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS | broad AIDE Lite tests |

No test failures were observed.
