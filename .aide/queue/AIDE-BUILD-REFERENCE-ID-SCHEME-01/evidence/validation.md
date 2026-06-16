# Validation

Status: PASS_WITH_WARNINGS.

Initial preflight before edits:

- `git status --short --branch`: PASS, clean on `main...origin/main`.
- `git rev-parse HEAD`: PASS, `f717851ecef2ae3c13f964bf8ee11a895ebf944d`.
- `git show --stat --oneline --name-status HEAD`: PASS, TestJob acceptance commit.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, `AIDE-ACCEPT-TESTJOB-SCHEMA-01` at `needs_review`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-TESTJOB-SCHEMA-01`: PASS, complete.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-TESTJOB-SCHEMA-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py test-job status`: PASS.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS.

Implementation validation run so far:

- `py -3 -m py_compile core/protocol/reference_id.py`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m py_compile core/protocol/reference_id.py .aide/scripts/tests/test_aide_reference_id_scheme.py .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m json.tool .aide/protocol/aide-reference-id.schema.json`: PASS.
- `py -3 .aide/scripts/aide_lite.py reference-id status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reference_id_scheme.py`: PASS, 20 tests.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `rg` scan for positive forbidden ReferenceID markers in `core/protocol/reference_id.py`, `.aide/reports/reference-id/**`, and `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/**`: PASS, no matches.
- `rg` scan for direct `AIDE-BUILD-EVENT-RECORD` recommendation in `core/protocol/reference_id.py`, `.aide/reports/reference-id/**`, and `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/**`: PASS, no matches.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.

Generated report churn from predecessor validation was restored for out-of-scope TestJob and WorkUnit queue reports before finalizing the task evidence.
