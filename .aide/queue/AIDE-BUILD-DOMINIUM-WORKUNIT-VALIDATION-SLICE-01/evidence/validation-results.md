# Validation Results

Pre-materialization checks:

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_workunit_validation_slice.py`: PASS, 5 tests.
- `py -3 -m py_compile core\interop\dominium\workunit_validation.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_workunit_validation_slice.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py dominium-workunit-validation run`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py dominium-workunit-validation validate`: PASS_WITH_WARNINGS.

Final checks:

- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 -m py_compile core\interop\dominium\workunit_validation.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_workunit_validation_slice.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_workunit_validation_slice.py`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py dominium-workunit-validation status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py dominium-workunit-validation run`: PASS_WITH_WARNINGS, `capability_invocation_count: 1`.
- `py -3 .aide/scripts/aide_lite.py dominium-workunit-validation validate`: PASS_WITH_WARNINGS, `error_count: 0`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py workunit inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam_repair_04.py`: PASS, 7 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam_repair_05.py`: PASS, 7 tests.
- Secret-like scan over new slice paths: no credentials found. Matches were denylist literals such as `secrets/**` and `credentials/**`.

Timed out and not claimed as passing:

- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam*.py"` exceeded 120s and 300s bounded runs.
- Exact-pattern bounded reruns of `test_aide_dominium_readonly_seam.py`, `test_aide_dominium_readonly_seam_repair.py`, `test_aide_dominium_readonly_seam_repair_02.py`, and `test_aide_dominium_readonly_seam_repair_03.py` exceeded 240s.
- Direct file execution of `test_aide_dominium_readonly_seam_repair_05.py` failed with `ModuleNotFoundError: No module named 'core'`; the same module passed under the supported `unittest discover` harness.

The timed-out historical seam modules are warning-class for this build because
the current slice's focused tests, generated validation, task inspection,
WorkUnit inspection, broad AIDE validation, and latest Repair 04/05 seam suites
passed.
