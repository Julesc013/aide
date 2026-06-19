# Validation

Validation commands run:

```text
py -3 -m py_compile core/protocol/conformance_result.py
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m py_compile .aide/scripts/tests/test_aide_conformance_result.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
py -3 .aide/scripts/aide_lite.py conformance-result status
py -3 .aide/scripts/aide_lite.py conformance-result project
py -3 .aide/scripts/aide_lite.py conformance-result validate
py -3 -m json.tool .aide/reports/conformance-result/results.json
py -3 -m json.tool .aide/reports/conformance-result/result-index.json
py -3 -m json.tool .aide/reports/conformance-result/case-result-index.json
py -3 -m json.tool .aide/reports/conformance-result/projection-report.json
py -3 -m json.tool .aide/reports/conformance-result/validation.json
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
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
git diff --check
git diff --cached --check
secret-like value scan over changed files
```

Observed status:

```text
PASS_WITH_WARNINGS
```

Focused test result:

```text
Ran 18 tests
OK
```

Generated predecessor validation churn outside this task scope was restored
after validation. `git diff --check` passed with the known queue-index
line-ending warning only; `git diff --cached --check` passed.
