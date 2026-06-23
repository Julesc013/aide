# Validation Results

Final command results:

- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, no missing evidence listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`: PASS, no missing evidence listed.
- Acceptance report/evidence local-path and secret-like scan: PASS, no matches.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Accepted invariants:

- source build result is `PASS_WITH_WARNINGS`;
- source check result is `PASS_WITH_WARNINGS`;
- source check material finding count is `0`;
- missing evidence is `0` for build, check, and acceptance;
- accepted capability is exactly `fixture_backed_dominium_validation_adapter`;
- acceptance reports contain no local absolute paths or secret-like values;
- broad AIDE validation passes.
