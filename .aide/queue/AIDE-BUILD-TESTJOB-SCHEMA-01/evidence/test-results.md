# Test Results

Status: PASS.

Commands run so far:

- `py -3 -m py_compile core/protocol/test_job.py`
  - Result: PASS
- `py -3 -m py_compile .aide/scripts/aide_lite.py`
  - Result: PASS
- `py -3 -m json.tool .aide/protocol/aide-test-job.schema.json`
  - Result: PASS
- `py -3 -m json.tool .aide/reports/test-job/projection-report.json`
  - Result: PASS
- `py -3 -m json.tool .aide/reports/test-job/validation.json`
  - Result: PASS
- `Get-ChildItem .aide\reports\test-job\projections\*.test-job.json | ForEach-Object { py -3 -m json.tool $_.FullName > $null }`
  - Result: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_test_job_schema.py`
  - Result: PASS
  - Summary: 29 focused TestJob tests passed.
- `py -3 .aide/scripts/aide_lite.py test --filter test_job`
  - Result: NOT RUN
  - Summary: helper filter is unsupported by the current test command surface.
- `py -3 .aide/scripts/aide_lite.py test-job status`
  - Result: PASS
- `py -3 .aide/scripts/aide_lite.py test-job project --source accepted-artifacts`
  - Result: PASS
  - Summary: 9 projections written; source reports not mutated.
- `py -3 .aide/scripts/aide_lite.py test-job validate`
  - Result: PASS
- `py -3 .aide/scripts/aide_lite.py worker-run validate`
  - Result: PASS
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`
  - Result: PASS
  - Summary: generated predecessor report churn was restored because it is outside this task.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`
  - Result: PASS
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`
  - Result: PASS
- `git diff --check`
  - Result: PASS

The focused tests cover schema shape, compatibility metadata, command/environment/framework/timeout/artifact/log/evidence fields, helper validation, fail-closed unknown required capabilities, additive projection, source non-mutation, CLI dispatch, unsupported runtime command rejection, report boundaries, deterministic paths, and secret-scan behavior.
