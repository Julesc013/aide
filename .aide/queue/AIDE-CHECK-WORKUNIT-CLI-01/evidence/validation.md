# Validation

Result: PASS_WITH_WARNINGS

Direct shell validation commands:
- `py -3 -m py_compile .aide/scripts/aide_lite.py core/protocol/envelope.py core/protocol/evidence_packet.py core/protocol/workunit.py core/protocol/workunit_cli.py`: PASS (exit 0)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_cli.py`: PASS (exit 0)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_workunit_queue_v1.py`: PASS (exit 0)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_evidence_packet_schema.py`: PASS (exit 0)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_contract_envelope.py`: PASS (exit 0)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py`: PASS (exit 0)
- `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections`: PASS (exit 0)
- `py -3 .aide/scripts/aide_lite.py validate`: PASS (exit 0)
- `py -3 .aide/scripts/aide_lite.py test`: PASS (exit 0)
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS (exit 0)
- `git diff --check`: PASS (exit 0)
- `git diff --check HEAD^ HEAD`: PASS (exit 0)

Warnings:
- .aide/context/latest-task-packet.md is stale and still references AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01.
- Nested Python subprocess invocation of py -3 selected Python 3.9.13 while direct PowerShell py -3 selected Python 3.14.5.
- Full JSON Schema Draft 2020-12 validation remains deferred by accepted predecessor scope.
