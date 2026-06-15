# Test And Validation Review

Result: PASS_WITH_WARNINGS.

Build and check evidence record these passing validations:

- `py -3 -m py_compile core/protocol/test_job.py`
- `py -3 -m py_compile .aide/scripts/aide_lite.py`
- `py -3 -m json.tool .aide/protocol/aide-test-job.schema.json`
- `py -3 -m json.tool .aide/reports/test-job/projection-report.json`
- `py -3 -m json.tool .aide/reports/test-job/validation.json`
- JSON parsing for `.aide/reports/test-job/projections/*.test-job.json`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_test_job_schema.py`, 29 tests
- `py -3 .aide/scripts/aide_lite.py test-job status`
- `py -3 .aide/scripts/aide_lite.py test-job project --source accepted-artifacts`
- `py -3 .aide/scripts/aide_lite.py test-job validate`
- `py -3 .aide/scripts/aide_lite.py worker-run validate`
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`
- unsupported `test-job submit/run/retry/summarize` fail-closed checks
- corrected secret and overclaim scans
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`

Warnings accepted as non-blocking:

- Full JSON Schema Draft 2020-12 validation remains deferred.
- TestJob is metadata-only.
- `.aide/context/latest-task-packet.md` is stale relative to queue truth.
- Initial check scan invocations were corrected and rerun.
- Generated report churn was restored by the check task and must continue to be contained.

Acceptance-local validation was run after artifact creation and is recorded in the final task report.
