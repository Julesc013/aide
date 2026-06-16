# Validation

Status: PASS_WITH_WARNINGS.

Preflight validation:

- Initial wrapper attempt: FAILED_WRAPPER, malformed PowerShell invocation; no command bodies were counted as validation.
- Corrected preflight runner: PASS for requested git, task, ReferenceID, predecessor validator, and broad repository validation commands.
- Preflight generated report churn outside this task scope was restored before acceptance artifacts were written.

Acceptance validation after artifact creation:

- `git status --short --branch`: PASS, expected acceptance artifacts and queue/log diffs only.
- `git diff --check`: PASS, with a line-ending warning for `.aide/queue/index.yaml`.
- `git diff --cached --check`: PASS.
- `py -3 -m json.tool .aide/reports/reference-id-accept/acceptance-report.json`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`: PASS, classification complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py reference-id status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Post-validation churn:

- `test-job validate` and `workunit-queue validate` refreshed `.aide/reports/test-job/projection-report.md` and `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`.
- Those diffs were out of scope for this acceptance task and were restored after validation.
