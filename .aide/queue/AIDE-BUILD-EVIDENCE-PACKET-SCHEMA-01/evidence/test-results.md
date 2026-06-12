# Test Results

Focused tests run before final validation:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py` | 0 | PASS | compile check |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py` | 0 | PASS | 35 tests |
| `py -3 .aide/scripts/aide_lite.py evidence-packet status` | 0 | PASS | thin dispatch |
| `py -3 .aide/scripts/aide_lite.py evidence-packet project --source accepted-slices` | 0 | PASS | 5 projections |
| `py -3 .aide/scripts/aide_lite.py evidence-packet validate` | 0 | PASS | schema/helper/projection validation |

Compatibility tests run during final validation:

| Command | Exit | Result | Notes |
| --- | ---: | --- | --- |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py` | 0 | PASS | 29 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | 0 | PASS | 17 tests |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | 0 | PASS | 37 tests |

All targeted tests passed.
