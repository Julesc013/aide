# Validation

Initial preflight:

- `git status --short --branch`: clean on `main...origin/main`
- `git rev-parse HEAD`: `f001fdeec978ed12c321ec83c1f43734a46ff77f`
- `git diff --check`: pass
- `git diff --cached --check`: pass
- predecessor validators: pass or pass with expected warnings

Live discrepancy recorded:

- The prompt reported `main` ahead of origin by one commit.
- Live repo state showed `main` tracking `origin/main` at `f001fde` with no
  ahead/behind marker.

Generated preflight churn restored:

- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-task-status.md`
- `.aide/reports/test-job/projection-report.md`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`

Post-implementation validation:

- `git diff --check`: pass
- `git diff --cached --check`: pass
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: pass
- `py -3 -m py_compile core/protocol/capability_manifest.py`: pass
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_capability_manifest.py`: pass, 11 tests
- `py -3 .aide/scripts/aide_lite.py capability-manifest status`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py capability-manifest project`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`: pass, `PASS_WITH_WARNINGS`
- `py -3 -m json.tool .aide/reports/capability-manifest/projection-report.json`: pass
- `py -3 -m json.tool .aide/reports/capability-manifest/validation.json`: pass
- `py -3 -m json.tool .aide/reports/capability-manifest/capabilities.json`: pass
- `py -3 -m json.tool .aide/reports/capability-manifest/capability-index.json`: pass
- `py -3 .aide/scripts/aide_lite.py reconciler validate`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py okf validate`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py okf lint`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py event-record validate`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: pass, `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py test-job validate`: pass
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: pass
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: pass
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: pass
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: pass
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: pass
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-CAPABILITY-MANIFEST-01`: pass
- `py -3 .aide/scripts/aide_lite.py validate`: pass, exit 0

Post-validation generated churn restored:

- `.aide/reports/test-job/projection-report.md`
- `.aide/reports/workunit-queue/projections/workunit-queue-build.workunit.json`
