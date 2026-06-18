# Validation

Result: `PASS_WITH_WARNINGS`

Commands run during this check:

```text
py -3 -m py_compile core/protocol/conformance_profile.py .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_profile.py
py -3 .aide/scripts/aide_lite.py conformance-profile status
py -3 .aide/scripts/aide_lite.py conformance-profile project
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py reconciler validate
py -3 .aide/scripts/aide_lite.py okf validate
py -3 .aide/scripts/aide_lite.py okf lint
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py workunit validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py contract-envelope validate
py -3 -m json.tool .aide/reports/conformance-profile/profiles.json
py -3 -m json.tool .aide/reports/conformance-profile/profile-index.json
py -3 -m json.tool .aide/reports/conformance-profile/case-index.json
py -3 -m json.tool .aide/reports/conformance-profile/projection-report.json
py -3 -m json.tool .aide/reports/conformance-profile/validation.json
py -3 -m json.tool .aide/reports/conformance-profile-check/check-report.json
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py validate
git diff --check
```

Observed results:

- focused unittest: `Ran 17 tests`; `OK`
- `conformance-profile status`: `PASS_WITH_WARNINGS`
- `conformance-profile project`: `PASS_WITH_WARNINGS`
- `conformance-profile validate`: `PASS_WITH_WARNINGS`
- determinism/source-mutation sentinel: `UNCHANGED`
- task inspect/evidence: `missing_evidence: 0`
- predecessor validators: pass or pass-with-warnings according to their existing warning posture
- broad `validate`: exit 0
- secret-like value scan over changed check surfaces: `NO_MATCHES`
- `git diff --check`: pass

Generated report churn outside the allowed check paths was restored after
validation.
