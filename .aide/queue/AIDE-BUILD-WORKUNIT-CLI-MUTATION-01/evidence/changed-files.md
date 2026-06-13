# Changed Files

- `.aide/scripts/aide_lite.py`: added dispatch/output for `workunit create`, `workunit block`, and `workunit evidence add`.
- `core/protocol/workunit_cli.py`: added queue metadata mutation helpers, safe path checks, reports, and mutation validation outputs.
- `.aide/scripts/tests/test_aide_workunit_cli.py`: updated read-only CLI compatibility expectations for the accepted mutation capability.
- `.aide/scripts/tests/test_aide_workunit_cli_mutation.py`: added focused temp-root mutation tests.
- `.aide/tmp/workunit-cli-mutation/safe-create-request.json`: repo-local dry-run create request fixture.
- `.aide/reports/workunit-cli-mutation/**`: generated command, validation, mutation-safety, and scan reports.
- `.aide/queue/AIDE-BUILD-WORKUNIT-CLI-MUTATION-01/**`: task scaffold and evidence.
- `.aide/queue/index.yaml`: registered this queue item and marked it `implementation_completed` / `PASS`.
