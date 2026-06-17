# Validation

Preflight:

- `git status --short --branch`: clean on `main...origin/main`
- `git remote -v`: origin fetch/push configured for `Julesc013/aide`
- `git rev-parse HEAD`: `2510d0d7d085ce71b32eaaa66858970a2d0edfa5`
- `git show --stat --oneline --name-status HEAD`: confirms
  `audit(protocol): add CapabilityManifest`
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; latest task packet
  selection remains stale and points to lifecycle fixture work
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py capability-manifest status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py capability-manifest project`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`: PASS_WITH_WARNINGS
- predecessor validators: PASS or PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, exit 0

Generated preflight churn restored before edits:

- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-task-status.md`
- `.aide/reports/test-job/projection-report.md`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`

Final validation after check artifacts were generated:

- `py -3 -m json.tool .aide/reports/capability-manifest-check/check-report.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/projection-report.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/validation.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/capabilities.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/capability-index.json`: PASS
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS
- `py -3 -m py_compile core/protocol/capability_manifest.py`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_capability_manifest.py`: PASS, 11 tests
- `py -3 .aide/scripts/aide_lite.py capability-manifest status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py capability-manifest project`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py reconciler validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py okf validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py okf lint`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py event-record validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, exit 0
- unsupported `capability-manifest run/execute/admit/conformance/adapter-run/repair/mutate`: fail closed with exit code 2
- `git diff --check`: PASS, with the existing queue-index CRLF normalization warning
- `git diff --cached --check`: PASS

Final generated validation churn restored:

- `.aide/reports/test-job/projection-report.md`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`

Non-blocking environment note:

- Two predecessor validator invocations printed an oh-my-posh init-file lock
  warning while still exiting 0. The AIDE command results were PASS or
  PASS_WITH_WARNINGS and no repo files were affected by that shell warning.
