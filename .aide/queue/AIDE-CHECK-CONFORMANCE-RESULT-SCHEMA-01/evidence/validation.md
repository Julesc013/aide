# Validation

Preflight validation passed:

```text
git status --short --branch
git remote -v
git rev-parse HEAD
git show --stat --oneline --name-status HEAD
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py task status
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
py -3 .aide/scripts/aide_lite.py conformance-result status
py -3 .aide/scripts/aide_lite.py conformance-result project
py -3 .aide/scripts/aide_lite.py conformance-result validate
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py reconciler validate
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py workunit-queue validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py contract-envelope validate
py -3 .aide/scripts/aide_lite.py validate
```

Independent check result:

```text
FAILED_VALIDATION
```

Cause:

```text
profile_digest_mismatch
```

Post-output validation passed:

```text
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core/protocol/conformance_result.py .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
py -3 -m json.tool .aide/reports/conformance-result-check/check-report.json
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
py -3 .aide/scripts/aide_lite.py conformance-result status
py -3 .aide/scripts/aide_lite.py conformance-result validate
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py reconciler validate
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py workunit-queue validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py contract-envelope validate
py -3 .aide/scripts/aide_lite.py validate
secret-like value scan over changed files
```

The validation commands pass for the check artifacts. The check finding remains
`FAILED_VALIDATION` because the independent raw-profile digest recomputation
does not match the ConformanceResult's recorded profile digest.
