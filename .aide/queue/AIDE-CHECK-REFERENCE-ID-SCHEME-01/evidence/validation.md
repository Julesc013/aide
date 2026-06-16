# Validation

Status: PASS_WITH_WARNINGS.

Preflight before check artifacts:

- `git status --short --branch`: PASS, clean on `main...origin/main`.
- `git remote -v`: PASS, `origin https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `ae1089bf4d56dd8b46b29ee152ed7c27c8d07f3e`.
- `git show --stat --oneline --name-status HEAD`: PASS, ReferenceID build commit.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, live queue includes `AIDE-BUILD-REFERENCE-ID-SCHEME-01`; latest task id remains stale lifecycle-runner text.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py reference-id status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Machine checks before check artifacts:

- `.aide/reports/reference-id/reference-map.json` parsed: PASS, 25 refs.
- Required locators missing: PASS, 0.
- Required locators without SHA-256: PASS, 0.
- `.aide/reports/reference-id/validation.json` parsed: PASS, status `PASS_WITH_WARNINGS`, validation errors 0.

Final validation after check artifacts is recorded by the final command batch and commit check.

Final validation after check artifacts:

- `py -3 -m py_compile core/protocol/reference_id.py`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_reference_id_scheme.py`: PASS, 20 tests.
- `py -3 -m json.tool .aide/reports/reference-id/projection-report.json`: PASS.
- `py -3 -m json.tool .aide/reports/reference-id/validation.json`: PASS.
- `py -3 -m json.tool .aide/reports/reference-id/reference-map.json`: PASS.
- `py -3 -m json.tool .aide/reports/reference-id-check/check-report.json`: PASS.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py reference-id status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id project`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REFERENCE-ID-SCHEME-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-REFERENCE-ID-SCHEME-01`: PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-REFERENCE-ID-SCHEME-01`: PASS, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `rg` scan for positive forbidden ReferenceID markers across ReferenceID helper/reports/build evidence/check evidence/check reports: PASS, no matches.
- `rg` scan for `AIDE-BUILD-EVENT-RECORD`: PASS_WITH_WARNINGS, matches only the allowed acceptance next-task prompt seed and an older build evidence note that says the prior direct EventRecord recommendation scan had no matches.
- `rg` scan for raw prompts/responses, private-key markers, and provider key patterns in check artifacts: PASS, no secret-like values found.
