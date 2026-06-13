# Changed Files

- `.aide/scripts/aide_lite.py`: thin dispatch for read-only `workunit` commands.
- `core/protocol/workunit_cli.py`: read-only helper and additive report writer.
- `core/protocol/__init__.py`: exports `workunit_cli`.
- `.aide/scripts/tests/test_aide_workunit_cli.py`: focused CLI/helper tests.
- `.aide/reports/workunit-cli/**`: generated read-only CLI reports.
- `.aide/queue/AIDE-BUILD-WORKUNIT-CLI-01/**`: task packet and evidence.
- `.aide/queue/index.yaml`: queue index entry.
