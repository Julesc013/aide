# Validation

## Preflight

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | clean before status/report refreshes; `## main...origin/main` |
| `git remote -v` | PASS | origin fetch/push configured |
| `git rev-parse HEAD` | PASS | `31e674562d1757e24fd072059e57392f7cac3401` |
| `git show --stat --oneline --name-status HEAD` | PASS | latest commit is `31e6745 audit(aide): checkpoint lifecycle fixture upgrade dry-run` |
| `git diff --check HEAD^ HEAD` | PASS | no whitespace errors |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 86 tasks before this WorkUnit was added |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | global selector still `AIDE-APPLY-LIFECYCLE-PLAN-01` |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | NOT_RUN | positional task id form unsupported by CLI |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | NOT_RUN | positional task id form unsupported by CLI |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | positional task id form unsupported by CLI |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | positional task id form unsupported by CLI |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | status `needs_review`, 15 evidence files, 0 missing |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | 15 evidence files |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | status `needs_review`, 13 evidence files, 0 missing |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | 13 evidence files |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | report-only, no mutation |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | full repo validation |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | target repo capable false; production-ready false; release-ready false |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | report-only; active repo apply false |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | report-only; real repo apply allowed false |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | lifecycle-schema subcommands: status, validate, fixture-verify |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | task subcommands include inspect, status, evidence, next-plan |

## Post-Work

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | PASS | no whitespace errors |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | status `needs_review`, classification `complete`, 16 evidence files, 0 missing |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | 16 evidence files available |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 87 tasks; latest task `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | global selector still `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch is `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | upstream checkpoint remains complete |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | 15 evidence files available |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | report-only; unchanged reports after final run |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | full repo validation; latest task packet tokens 1761 |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | target repo capable false; broad active repo apply false; production-ready false; release-ready false |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | report-only; active repo apply false |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | report-only; real repo apply allowed false |
| JSON parse for repair reports, repair plans, plan reports, and scenarios | PASS | 15 JSON files parsed before final report set; repair report no-apply fields checked across 10 files |
| focused repair scenario consistency check | PASS | 2 repair scenarios verified; hashes, markers, reports, paths, and no-apply fields match |
| YAML structural fallback check | PASS | task/status/index surfaces contain required structural keys; PyYAML unavailable |
| Boundary text search | PASS_WITH_NOTES | initial strict scan flagged lifecycle-schema lines saying enabling markers are omitted; contextual rerun passed across 34 files |
| Secret scan over changed files | PASS | no credential-like assignments found |
| `py -3 .aide/scripts/aide_lite.py lifecycle-repair status/dry-run/verify` | NOT_RUN | no `lifecycle-repair` command was implemented or authorized in this report-only task |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | no Python code changed |
| focused lifecycle repair dry-run tests | NOT_RUN | no code or test paths were changed |
