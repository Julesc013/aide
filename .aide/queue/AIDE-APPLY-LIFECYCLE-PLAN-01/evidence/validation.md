# Validation

Validation results are recorded after final command execution. Initial preflight passed:

- `git status --short --branch` - PASS, initial status `## main...origin/main`.
- `git remote -v` - PASS, origin fetch/push `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD` - PASS, initial HEAD `2a095036f8bb12f7010e53c9e1a207db700b1358`.
- `git show --stat --oneline --name-status HEAD` - PASS, latest commit `2a09503 fix(task-os): repair current latest task reporting`.
- `git diff --check HEAD^ HEAD` - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS, latest task before this task was `AIDE-TASK-OS-STATUS-REPAIR-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS, selected `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - PASS, evidence complete.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-QUEUE-CLOSURE-02` - PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-QUEUE-CLOSURE-02` - PASS, evidence complete.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0` - PASS, complete, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0` - PASS, evidence complete.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only.

The prompt's positional `task inspect AIDE-...` and `task evidence AIDE-...` forms were not used because the live CLI requires `--task-id`.

## Final Validation

- `git status --short --branch` - PASS before commit, worktree contained only task-scoped changes plus authorized Task OS reports and new task files.
- `git diff --check` - PASS.
- `git diff --check HEAD^ HEAD` - PASS for latest committed parent work.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS. Task count 76. Latest task ID `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS. The command still selects `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`; this is recorded as a warning because this task is not authorized to update Task OS selector implementation. The lifecycle plan's own `next-batch.md` selects `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-LIFECYCLE-PLAN-01` - PASS. Status `needs_review`, classification `complete`, evidence files 8, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-LIFECYCLE-PLAN-01` - PASS. Evidence present and missing none.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only; target mutation false, broad active-repo apply false, production-ready false, release-ready false.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only; active repo apply false, target mutation false.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only; real repo apply false.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 -c "import json ... lifecycle-graph.json"` - PASS. Nodes 15, edges 14.
- `py -3 -c "import pathlib, yaml ..."` - NOT_RUN/PyYAML unavailable; failed with `ModuleNotFoundError: No module named 'yaml'`.
- `py -3 -c` structural YAML sanity check over `.aide/queue/index.yaml`, task `task.yaml`, and task `status.yaml` - PASS.
- Boundary text search over changed files - PASS for all required terms, including `AIDE-APPLY-LIFECYCLE-PLAN-01`, `lifecycle planning`, `install apply`, `upgrade apply`, `lifecycle repair apply`, `rollback apply`, `uninstall apply`, `fixture`, `dry-run`, `rollback-compatible`, `target repo`, `active repo`, `token quality ledger`, `allowed paths`, `protected paths`, `forbidden operations`, `review gate`, `needs_review`, `production-ready`, `release-ready`, `broad active-repo apply`, `provider/model calls`, `Gateway calls`, and `network calls`.
- Broad changed-file secret scan - PASS. Files scanned: 21, secret hits: 0.
- Diff-added-line secret scan - PASS. `diff_added_secret_hits: 0`.

## Generated Report Churn

Required status commands refreshed `current_commit` stamps in non-Task-OS reports. Those out-of-scope changes were restored. Retained generated reports are limited to authorized Task OS report files.
