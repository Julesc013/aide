# Validation

Final validation completed:

```text
py -3 -m py_compile core/protocol/conformance_profile.py
PASS

py -3 -m py_compile .aide/scripts/aide_lite.py
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_profile.py
PASS

py -3 .aide/scripts/aide_lite.py conformance-profile project
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py conformance-profile validate
PASS_WITH_WARNINGS

py -3 -m json.tool .aide/reports/conformance-profile/profiles.json
PASS

py -3 -m json.tool .aide/reports/conformance-profile/profile-index.json
PASS

py -3 -m json.tool .aide/reports/conformance-profile/case-index.json
PASS

py -3 -m json.tool .aide/reports/conformance-profile/projection-report.json
PASS

py -3 -m json.tool .aide/reports/conformance-profile/validation.json
PASS

py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONFORMANCE-PROFILE-01
PASS: status needs_review, classification complete, evidence_files 22, missing_evidence 0

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONFORMANCE-PROFILE-01
PASS: 22 available, 0 missing

py -3 .aide/scripts/aide_lite.py contract-envelope validate
PASS

py -3 .aide/scripts/aide_lite.py evidence-packet validate
PASS

py -3 .aide/scripts/aide_lite.py workunit validate
PASS

py -3 .aide/scripts/aide_lite.py worker-run validate
PASS

py -3 .aide/scripts/aide_lite.py test-job validate
PASS

py -3 .aide/scripts/aide_lite.py reference-id validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py event-record validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py okf validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py okf lint
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py reconciler validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py capability-manifest validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py validate
PASS

determinism check over ConformanceProfile JSON reports
PASS

secret-like value scan over changed files
PASS

git diff --check
PASS with existing CRLF notice for .aide/queue/index.yaml

git diff --cached --check
PASS
```

Validation warnings are expected for profile-only status, accepted predecessor
warning debt, and existing predecessor warning-bearing validators. No blockers or
errors were found.
