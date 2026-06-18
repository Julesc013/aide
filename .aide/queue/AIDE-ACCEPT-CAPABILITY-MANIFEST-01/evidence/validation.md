# Validation

Final validation status: `PASS_WITH_WARNINGS`

Preflight before edits:

- `git status --short --branch`: PASS; generated git-plan helper reports were
  modified by the required branch-sensitive preflight.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, dry-run helper plan only.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-CAPABILITY-MANIFEST-01`: reported missing task surfaces, which this task materialized.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-CAPABILITY-MANIFEST-01`: reported missing evidence before this task.
- `task.yaml`, `status.yaml`, `ExecPlan.md`, `prompt.md`, and evidence for build/check predecessors were reviewed.

Post-report validation:

- `py -3 -m json.tool .aide/reports/capability-manifest-accept/acceptance-report.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/validation.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest/capabilities.json`: PASS
- `py -3 -m json.tool .aide/reports/capability-manifest-check/check-report.json`: PASS
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
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-CAPABILITY-MANIFEST-01`: PASS
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-CAPABILITY-MANIFEST-01`: PASS
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
- `py -3 .aide/scripts/aide_lite.py validate`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- secret-like value scan over changed files: PASS, no matches

Generated report churn outside the acceptance deliverable was restored before
final commit.
