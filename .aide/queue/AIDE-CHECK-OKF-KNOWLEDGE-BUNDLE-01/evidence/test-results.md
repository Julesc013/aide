# Test Results

Result: `PASS_WITH_WARNINGS`.

Commands run during the check:

```bat
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core/knowledge/okf_bundle.py
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_okf_knowledge_bundle.py
py -3 .aide/scripts/aide_lite.py okf status
py -3 .aide/scripts/aide_lite.py okf project --source current-repo
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
py -3 -m json.tool .aide/reports/okf/projection-report.json
py -3 -m json.tool .aide/reports/okf/validation.json
py -3 -m json.tool .aide/reports/okf/lint.json
py -3 -m json.tool .aide/reports/okf/concept-index.json
py -3 -m json.tool .aide/reports/okf/link-index.json
py -3 -m json.tool .aide/reports/okf-check/check-report.json
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01
py -3 .aide/scripts/aide_lite.py validate
```

Observed material results:

- focused OKF unittest file: PASS, 8 tests
- `okf status`: `PASS_WITH_WARNINGS`, concept count `24`
- `okf project --source current-repo`: `PASS_WITH_WARNINGS`, source artifacts mutated `false`
- `okf validate`: `PASS_WITH_WARNINGS`
- `okf lint`: `PASS_WITH_WARNINGS`
- JSON report parsing: PASS
- broad repository validation: PASS

Generated predecessor report churn from validation was restored when outside the check scope. Generated OKF page `source_hashes` refreshed after this check added its queue index entry and were restored because this check does not update OKF build outputs.
