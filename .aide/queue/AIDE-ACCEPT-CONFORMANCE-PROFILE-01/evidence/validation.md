# Validation

Result: `PASS_WITH_WARNINGS`

Commands run:

```text
git status --short --branch
git remote -v
git rev-parse HEAD
git show --stat --oneline --name-status HEAD
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py task status
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CONFORMANCE-PROFILE-01
py -3 -m py_compile core/protocol/conformance_profile.py
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_profile.py
py -3 -m json.tool .aide/reports/conformance-profile-accept/acceptance-report.json
py -3 -m json.tool .aide/reports/conformance-profile/projection-report.json
py -3 -m json.tool .aide/reports/conformance-profile/validation.json
py -3 -m json.tool .aide/reports/conformance-profile/profiles.json
py -3 -m json.tool .aide/reports/conformance-profile/profile-index.json
py -3 -m json.tool .aide/reports/conformance-profile/case-index.json
py -3 -m json.tool .aide/reports/conformance-profile-check/check-report.json
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-CONFORMANCE-PROFILE-01
py -3 .aide/scripts/aide_lite.py conformance-profile status
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
secret-like value scan over changed acceptance surfaces
```

Observed results:

- focused ConformanceProfile tests: `Ran 17 tests`; `OK`
- `conformance-profile status`: `PASS_WITH_WARNINGS`
- `conformance-profile validate`: `PASS_WITH_WARNINGS`
- predecessor validators: pass or expected pass-with-warnings
- broad `validate`: pass
- report JSON parsing: pass
- read-only source/report hash compare: `UNCHANGED`
- secret-like value scan: `NO_MATCHES`

Post-materialization results:

- acceptance task inspect/evidence: `classification: complete`, `status:
  needs_review`, `missing_evidence: 0`
- generated validation churn outside the allowed acceptance paths: restored
  before staging
- `git diff --check`: passed with the existing queue-index line-ending warning
- `git diff --cached --check`: run after staging
- commit policy check: run after the acceptance commit exists and reported with
  the final task result
