# Expected Vs Actual Validation

| Command | Expected Result | Actual Result | Notes |
| --- | --- | --- | --- |
| `git status --short --branch` | PASS_WITH_EXPECTED_CHANGES | PASS_WITH_EXPECTED_CHANGES | Shows checkpoint queue files, index/latest packet updates, and deterministic report refreshes on `main...origin/main [ahead 1]`. |
| `git diff --check` | PASS | PASS | Whitespace check passed. |
| `git diff --cached --check` | PASS | PASS | No staged whitespace errors. |
| `git diff --check HEAD^ HEAD` | PASS | PASS | Prior commit diff has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | PASS | Lists 92 tasks and latest task `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_KNOWN_WARNING | PASS_WITH_KNOWN_WARNING | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next WorkUnit remains `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01` | PASS | PASS | Checkpoint is complete with 18 evidence files and no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01` | PASS | PASS | Evidence directory lists 18 files and no missing evidence. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` | PASS | PASS | Preflight confirmed prior task is complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` | PASS | PASS | Preflight confirmed 16 evidence files. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | PASS | Preflight and post-change validation passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | PASS | Lifecycle schema status passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | PASS | 280 checks passed using stdlib structural fallback. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | PASS | 298 checks passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | PASS | Scoped transaction status passed; target repo capable remains false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | PASS | Managed-section status passed; active repo apply remains false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | PASS | Transaction status passed; real repo apply remains false. |
| Rollback JSON parse | PASS | PASS | Parsed 11 rollback dry-run JSON reports; no execution/enabling true flags found. |
| Rollback record JSON parse | PASS | PASS | Parsed 3 rollback-compatible records. |
| Boundary search | PASS | PASS | Boundary terms appear as blocked, deferred, non-goal, prohibited, report-only, or no-execution concepts. |
| Secret scan | PASS_WITH_FALSE_POSITIVES | PASS_WITH_FALSE_POSITIVES | Hits were `TOKEN_ESTIMATE` in latest packet and the literal scanner pattern in this evidence file. No real secrets found. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS | PENDING | Run after commit. |
