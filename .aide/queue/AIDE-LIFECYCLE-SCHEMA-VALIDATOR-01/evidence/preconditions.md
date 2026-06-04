# Preconditions

| Check | Result | Evidence |
| --- | --- | --- |
| Upstream lifecycle schema task exists | PASS | `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/task.yaml` |
| Upstream task selected this validator | PASS | `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/next-batch.md` |
| `.aide/queue/current.toml` absent | PASS | `Test-Path` returned `False`. |
| Validator task absent before this task | PASS | `Test-Path .aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` returned `False`. |
| Worktree started clean | PASS | Preflight `git status --short --branch` returned only `## main...origin/main`. |
| `json` available | PASS | `py -3 -c "import json"` succeeded. |
| `jsonschema` unavailable | WARN | `py -3 -c "import jsonschema"` failed with `ModuleNotFoundError`; stdlib fallback was implemented. |
| Task OS next-plan truth lag | WARN | `task next-plan` still selected `AIDE-APPLY-LIFECYCLE-PLAN-01`; upstream task-local next batch selected this validator. |
