# Validation

Initial and independent recheck validation passed:

```text
git status --short --branch
git rev-parse HEAD
git show --stat --oneline --name-status --no-renames HEAD
py -3 .aide/scripts/aide_lite.py task status
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
independent repair digest recheck
```

Post-output validation passed:

```text
git diff --check
git diff --cached --check
py -3 -m py_compile core/protocol/conformance_result.py .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
py -3 -m json.tool .aide/reports/conformance-result-repair-check/check-report.json
py -3 .aide/scripts/aide_lite.py conformance-result status
py -3 .aide/scripts/aide_lite.py conformance-result project
py -3 .aide/scripts/aide_lite.py conformance-result validate
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
py -3 .aide/scripts/aide_lite.py validate
secret-like value scan over changed files
```

Validation result:

```text
PASS_WITH_WARNINGS
```

The warnings are retained non-capability boundaries, not validation failures.
