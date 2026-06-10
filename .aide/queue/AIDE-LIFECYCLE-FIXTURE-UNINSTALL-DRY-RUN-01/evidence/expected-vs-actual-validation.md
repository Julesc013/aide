# Expected Vs Actual Validation

| Command | Expected Result | Actual Result | Notes |
| --- | --- | --- | --- |
| `git diff --check` | PASS | PASS | Whitespace check passed. |
| `task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` | PASS | PASS | Task is complete with 14 evidence files and no missing evidence. |
| `task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` | PASS | PASS | Evidence directory lists expected files. |
| `validate` | PASS | PASS | Repo validation passed. |
| `lifecycle-schema validate` | PASS | PASS | 280 checks passed. |
| `lifecycle-schema fixture-verify` | PASS | PASS | 298 checks passed. |
| JSON parse | PASS | PASS | Parsed 8 uninstall reports plus source plan/report inputs. |
| Enabling-marker search | PASS | PASS | No execution/mutation/readiness true flags found. |
| Boundary search | PASS | PASS | Boundary terms appear only as blocked/deferred/non-goal/prohibited/report-only concepts. |
| Secret scan | PASS_WITH_FALSE_POSITIVES | PASS_WITH_FALSE_POSITIVE | Only `TOKEN_ESTIMATE` metadata in the latest task packet matched. |
| `commit check --latest` | PASS | PENDING | Run after commit. |
