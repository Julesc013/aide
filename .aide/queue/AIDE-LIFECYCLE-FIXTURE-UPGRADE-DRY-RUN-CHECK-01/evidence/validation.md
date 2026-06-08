# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `706f50efbf581401a06630ea4701294857d9a298`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the upgrade dry-run WorkUnit. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in latest commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 85 tasks; latest task ID was `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | 14 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | 13 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |
| Independent upgrade dry-run static review | PASS_WITH_WARNINGS | 3 upgrade scenarios checked; 1 missing static expected report ref; 0 defects. |

Post-change validation is recorded after final validation runs in this same file before commit.

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected checkpoint artifacts, queue/context updates, and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged whitespace errors; nothing staged at the time. |
| `git diff --check HEAD^ HEAD` | PASS | Previous upgrade dry-run commit has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 86 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this checkpoint uses local `next-batch.md`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 15 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | Status `needs_review`; classification complete; 14 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | 14 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repository validation passed. |
| JSON parse and no-apply proof check | PASS | Parsed 16 JSON files: upgrade dry-run reports, generated upgrade plans, static expected upgrade reports, and scenario metadata; no top-level no-apply booleans were enabled. |
| Boundary text search | PASS | 36 checkpoint/report files checked; required concepts are represented; no enabling markers found. |
| Secret scan over changed/reviewed files | PASS | `rg --pcre2` found no credential-like assignments for secret/token/API key patterns. |
| YAML surface check | PASS_WITH_NOTES | Structural check confirmed task ID, allowed paths, protected paths, forbidden operations, status, result, and review gate; full YAML parse not available because PyYAML is not installed. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | No Python implementation files changed in this task. |

Validation warning:

- An initial boundary text search missed the exact phrase `expected upgrade report`; evidence wording was updated and the corrected boundary search passed.
