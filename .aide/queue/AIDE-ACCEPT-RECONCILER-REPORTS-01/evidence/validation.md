# Validation

Final validation status: `PASS_WITH_WARNINGS`

Preflight before edits:

- `git status --short --branch`: PASS
- `git remote -v`: PASS
- `git rev-parse HEAD`: PASS
- `git show --stat --oneline --name-status HEAD`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- `task status`: PASS with stale latest task packet observed
- `task inspect/evidence` for build and check tasks: PASS
- `reconciler status/report/validate`: PASS_WITH_WARNINGS
- predecessor validators: PASS or PASS_WITH_WARNINGS
- broad `validate`: PASS

Post-report validation:

- `py -3 -m json.tool .aide/reports/reconciler-accept/acceptance-report.json`: PASS
- `task inspect --task-id AIDE-ACCEPT-RECONCILER-REPORTS-01`: PASS
- `task evidence --task-id AIDE-ACCEPT-RECONCILER-REPORTS-01`: PASS
- `reconciler status`: PASS_WITH_WARNINGS
- `reconciler validate`: PASS_WITH_WARNINGS
- `okf validate`: PASS_WITH_WARNINGS
- `okf lint`: PASS_WITH_WARNINGS
- `event-record validate`: PASS_WITH_WARNINGS
- `reference-id validate`: PASS_WITH_WARNINGS
- `test-job validate`: PASS
- `worker-run validate`: PASS
- `workunit-queue validate`: PASS
- `evidence-packet validate`: PASS
- `contract-envelope validate`: PASS
- broad `validate`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS

Generated report churn outside the acceptance deliverable was restored.
