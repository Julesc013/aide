# Validation

## Preflight

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Preflight was clean: `## main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push remote present. |
| `git rev-parse HEAD` | PASS | Initial HEAD `d2ffd61b1b9e1a10267e1e027e967998edb458fd`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Prior checkpoint commit inspected. |
| `git diff --check HEAD^ HEAD` | PASS | No output. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 80 tasks before this task; latest task was checkpoint. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_WARNINGS | Global selector still selected `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local checkpoint selected this plan generator. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-CHECK-01` | NOT_RUN | Positional form is unsupported and returned an argument error. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-CHECK-01` | NOT_RUN | Positional form is unsupported and returned an argument error. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | Status `needs_review`, classification `complete`, evidence files 11, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01` | PASS | Evidence listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Status `needs_review`, classification `complete`, evidence files 9, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Evidence listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; lifecycle apply false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, shape-only. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Report-only; target mutation false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Report-only; active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply false. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Repo validation passed. |

## Final Checks

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_EXPECTED_CHANGES | Shows plan-generator task files, generated plans/reports, latest packet/index updates, and deterministic report refreshes. |
| `git diff --check` | PASS | No output. |
| `git diff --cached --check` | PASS | No staged changes at time of check; no output. |
| `git diff --check HEAD^ HEAD` | PASS | No output. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 81 tasks; latest task `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_WARNINGS | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch selects `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | Status `needs_review`, classification `complete`, evidence files 9, missing 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | 9 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Unchanged report; no apply or mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Report-only; no target/branch/provider/Gateway/network mutation. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Report-only; active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply false. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Latest task packet tokens `1176`. |

## Plan Artifact Checks

| Check | Result | Notes |
| --- | --- | --- |
| Mechanical generation | PASS | Generated 13 plans under `.aide/examples/apply/lifecycle-fixtures/generated-plans/**` and reports under `.aide/reports/lifecycle-fixture-plans/**`. |
| Generated plan structural validation | PASS | 13 plans, 15 generated report JSON files, scenario coverage `13/13`, no errors. |
| Changed JSON/YAML parse | PASS | 67 changed/untracked files seen, 32 JSON files parsed, 3 YAML files structurally checked, 13 generated plans checked. |
| Plan generator CLI commands | NOT_RUN | No `lifecycle-fixture` CLI command was implemented in this task. |
| Python compile/tests | NOT_RUN | No source code or tests changed. |

## Boundary Search

Command: `rg -n -i -F` over changed/generated files for the required boundary terms.

Result: PASS. All required terms were found, including `rollback apply` after the explicit wording update. Prohibited terms appear as non-goals, prohibited operations, false flags, blocked scenarios, or review-gated capability labels.

## Secret Scan

Command: `rg -n -i -e "SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY"` over changed/generated files.

Result: PASS_WITH_WARNINGS. Scanned 67 files with 51 marker hits. Hits are protected-path metadata, token-budget/task-name words, and generated blocked-path examples such as `secrets/example.env`; no credential material was found.

## Generated Report Churn

Required status and validation commands refreshed deterministic generated reports under `.aide/reports/**`. Those changes are retained as task evidence under the allowed path packet.
