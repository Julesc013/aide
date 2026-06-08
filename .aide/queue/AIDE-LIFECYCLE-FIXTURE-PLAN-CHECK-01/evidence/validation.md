# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status clean on `main...origin/main`; later report-only commands refreshed generated reports. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `ded7fbc75180e99f39bf1a6e294e6f84e3e58c52`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit generated lifecycle fixture plans. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in latest commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 81 tasks; latest task ID was `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task current` | PASS | Current task reported as `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | 9 evidence files, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | 11 evidence files, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks, stdlib structural fallback. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Review gate `needs_review`; target repo capable false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only, real repo apply allowed false. |
| local generated plan consistency script | PASS_WITH_NOTES | First strict run noted index does not duplicate per-plan `target_files_mutated_expected=false`; plan set otherwise passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Commands: status, validate, fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |

Final validation is recorded after all checkpoint files are written.

Post-change commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_NOTES | Shows checkpoint files, queue/latest-task updates, and deterministic report refreshes pending commit. |
| `git diff --check` | PASS | No whitespace errors. |
| `git diff --cached --check` | PASS | No staged whitespace errors before staging. |
| `git diff --check HEAD^ HEAD` | PASS | Prior commit remains clean. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 82 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch is `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | Classification complete, 11 evidence files, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | 11 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | 9 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; no lifecycle apply execution. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; no lifecycle apply execution. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo managed-section apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| local JSON/YAML parse checks | PASS | 41 JSON files parsed; 3 YAML surfaces checked. |
| local generated plan consistency script | PASS_WITH_NOTES | 13 plans, 13 index entries, 13 scenarios; no errors; index note recorded. |
| local expected report/rollback cross-check | PASS | 7 expected reports and 2 rollback records checked. |
| boundary text search | PASS | 54 files checked; required terms present; no enabling mutation markers found. |
| simple secret marker scan | PASS_WITH_NOTES | Hits were policy/boundary terms such as `secrets/**` and `secret scan`. |
| assignment-like credential scan | PASS | 37 files checked; 0 assignment-like credential hits. |
