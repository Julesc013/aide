# Validation

Result: PASS_WITH_WARNINGS.

Structural checks:

- `py -3 -m json.tool .aide/reports/test-job-accept/acceptance-report.json`
  - Result: PASS.
- `git diff --check`
  - Result: PASS, with a non-failing line-ending warning for `.aide/queue/index.yaml`.
- `git diff --cached --check`
  - Result: PASS.

Task evidence checks:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-TESTJOB-SCHEMA-01`
  - Initial result: partial, missing `changed-files.md` and `validation.md`.
  - Disposition: both standard evidence files were added.
  - Final result: PASS, classification `complete`, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-TESTJOB-SCHEMA-01`
  - Initial result: missing `changed-files.md` and `validation.md`.
  - Disposition: both standard evidence files were added.
  - Final result: PASS, missing evidence 0.

Protocol checks:

- `py -3 .aide/scripts/aide_lite.py test-job status`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py test-job validate`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`
  - Result: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`
  - Result: PASS.

Generated report churn:

- `.aide/reports/test-job/projection-report.md` was refreshed by validation and restored because it is outside this task's write scope.
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json` was refreshed by validation and restored because it is outside this task's write scope.

Warnings:

- Full JSON Schema Draft 2020-12 validation remains deferred.
- The TestJob slice remains metadata-only.
- `.aide/context/latest-task-packet.md` is stale relative to live queue truth.
- The next task is `AIDE-BUILD-REFERENCE-ID-SCHEME-01`, not PatchTransaction.
