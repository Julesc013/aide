# Validation

## Preflight

- `git status --short --branch` - PASS; initial worktree clean on `main...origin/main`.
- `git remote -v` - PASS; origin fetch/push configured.
- `git rev-parse HEAD` - PASS; initial HEAD `3fcceeb8b9d68eca12812930e60a039010b22e01`.
- `git show --stat --oneline --name-status HEAD` - PASS; prior commit was `3fcceeb docs(apply): define lifecycle proof ladder`.
- `git diff --check HEAD^ HEAD` - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; 76 tasks before this task, latest task `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS_WITH_WARNINGS; Task OS selected `AIDE-APPLY-LIFECYCLE-PLAN-01`, while that task's `next-batch.md` selected this task.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-APPLY-LIFECYCLE-PLAN-01` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-APPLY-LIFECYCLE-PLAN-01` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-LIFECYCLE-PLAN-01` - PASS.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-LIFECYCLE-PLAN-01` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-APPLY-02-scoped-transaction-executor-v0` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-APPLY-02-scoped-transaction-executor-v0` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0` - PASS.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0` - PASS.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS.

## Post-Change

- `git status --short --branch` - PASS_WITH_CHANGES; expected task files, schema files, examples, docs, index, latest task packet, README, and authorized generated reports changed.
- `git diff --check` - PASS.
- `git diff --cached --check` - PASS; no staged changes.
- `git diff --check HEAD^ HEAD` - PASS.
- JSON parse over lifecycle graph, lifecycle schemas, and lifecycle examples - PASS.
- YAML structural tab check over task/status/index YAML - PASS.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; 77 tasks, latest indexed task `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS_WITH_WARNINGS; Task OS still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`, a known selector lag.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` - NOT_RUN as written; command requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` - PASS; classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` - PASS; eight evidence files available, missing list empty.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS; report unchanged on rerun, no target mutation, branch mutation, provider/model calls, Gateway calls, or network calls.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS; reports unchanged on rerun, report-only.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS; reports unchanged on rerun, report-only.
- `py -3 -c "import importlib.util; ..."` - PASS; `jsonschema_available=False`, `yaml_available=False`.
- Boundary term scan over changed files - PASS for all required terms.
- Changed-file secret scan with `rg -n -i --pcre2 "SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY"` - REVIEW_WITH_FALSE_POSITIVES only; matches were boundary words such as `secrets`, `TOKEN_ESTIMATE`, token-ledger references, and `secret_scan_passed`, not credentials or key material.

## Generated Report Churn

Generated report changes are retained because this task explicitly authorizes `.aide/reports/task-os-*`, `.aide/reports/scoped-transaction-executor-*`, `.aide/reports/managed-section-*`, `.aide/reports/transaction-*`, and `.aide/reports/current-aide-roadmap.md` outputs from validation/status commands.
