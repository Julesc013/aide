# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`; live status did not show the user-provided `[ahead 1]` note. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `4a40217e48b632fcb565563735c5046559ee55ff`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the repair dry-run checkpoint. |
| `git diff --check HEAD^ HEAD` | PASS | Previous repair dry-run checkpoint commit has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 88 tasks; latest task ID was `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | Status `needs_review`; classification complete; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` | PASS | 9 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS_WITH_WARNINGS | Full validation passed; known compact task packet token warning remains. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Available lifecycle-schema subcommands are status, validate, and fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |
| Independent rollback record consistency check | PASS | 3 records, 2 fixture records, 13 generated plans, 7 expected reports, 2 linked fixture records. |

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected checkpoint artifacts, queue/context updates, and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged whitespace errors; nothing staged at the time. |
| `git diff --check HEAD^ HEAD` | PASS | Previous repair dry-run checkpoint commit has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 89 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this checkpoint uses local `next-batch.md`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` | PASS | Status `needs_review`; classification complete; 17 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` | PASS | 17 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 15 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS_WITH_WARNINGS | Full validation passed; known warning remains `compact task packet over target: 1887 > 1800`, while latest task packet passed at 1887 tokens. |
| Rollback record independent consistency check | PASS | 3 records, 2 fixture records, 13 generated plans, 7 expected reports, 2 linked fixture records. |
| Changed JSON parse and YAML surface check | PASS | Parsed 3 changed JSON files; task/status YAML surfaces include required checkpoint fields. |
| Boundary text search | PASS | 39 terms checked across checkpoint files and rollback record artifacts; required concepts are represented as blocked, planned-only, review-only, or prohibited. |
| Secret scan over changed files and rollback artifacts | PASS | 49 files scanned with 10 credential-marker assignment patterns; no matches. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | No Python implementation files changed in this checkpoint. |

Validation warnings:

- Rollback records are static compatibility examples only; no rollback dry-run harness consumed them in this checkpoint.
- `rollback_apply_executed` is not a required record-schema field; no-execution evidence is represented by `rollback_execution_implemented=false` in records and no-mutation/no-execution fields in surrounding plans and reports.
- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- Full validation reports the known compact task packet token warning.
