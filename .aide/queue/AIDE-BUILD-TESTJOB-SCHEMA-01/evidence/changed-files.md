# Changed Files

Task: AIDE-BUILD-TESTJOB-SCHEMA-01
Result: PASS

## Source

- `core/protocol/test_job.py`: added metadata-only TestJob helper, schema subset validation, projection, status, and validation report functions.
- `core/protocol/__init__.py`: exported `test_job`.
- `.aide/scripts/aide_lite.py`: added thin `test-job status/project/validate` CLI dispatch.
- `.aide/scripts/tests/test_aide_test_job_schema.py`: added focused TestJob schema/helper/projection/CLI tests.

## Schema

- `.aide/protocol/aide-test-job.schema.json`: added minimal envelope-backed TestJob schema.

## Reports

- `.aide/reports/test-job/status.md`: status surface for the minimal TestJob slice.
- `.aide/reports/test-job/projection-report.json`: machine-readable projection report.
- `.aide/reports/test-job/projection-report.md`: human-readable projection report.
- `.aide/reports/test-job/validation.json`: machine-readable validation report.
- `.aide/reports/test-job/validation.md`: human-readable validation report.
- `.aide/reports/test-job/future-work.md`: future protocol/runtime sequence.
- `.aide/reports/test-job/unfinished-work.md`: explicit unfinished runtime work.
- `.aide/reports/test-job/projections/*.test-job.json`: additive metadata-only TestJob projections.

## Queue And Evidence

- `.aide/queue/AIDE-BUILD-TESTJOB-SCHEMA-01/**`: task packet, ExecPlan, status, prompt, and evidence.
- `.aide/queue/index.yaml`: added the build task entry.

## Root Indexes

- `PLANS.md`: added the bounded TestJob queue plan entry.
- `IMPLEMENT.md`: added the implementation log entry.
- `DOCUMENTATION.md`: added the documentation index note for the TestJob protocol slice.
