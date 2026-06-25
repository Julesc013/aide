# Validation Results

- PASS: focused local service tests, 7 tests.
- PASS_WITH_WARNINGS: local-service init-fixture.
- PASS_WITH_WARNINGS: local-service fixture.
- PASS_WITH_WARNINGS: local-service status.
- PASS_WITH_WARNINGS: local-service validate.
- PASS: compileall for `core/service` and `.aide/scripts/tests`.
- PASS: trust authorization regression tests.
- PASS: local process execution host regression tests.
- PASS: task inspect reported classification `complete` and `missing_evidence: 0`.
- PASS: task evidence reported no missing evidence files.
- PASS: broad `aide_lite.py validate`.
- PASS: `git diff --check`.
- PASS: `git diff --cached --check`.
- PASS: `.aide.local/service` absent after fixture execution.
- PASS: absolute local path scan over local service files, reports, tests, and task evidence.
- PASS: strict secret-like scan over local service files, reports, tests, and task evidence.
