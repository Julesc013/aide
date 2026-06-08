# Validation

Pre-check validation was run before creating upgrade dry-run artifacts:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `8c97beb9f4b4f85c9413f17d73d72b87296adb7f`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the lifecycle fixture install dry-run checkpoint. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in latest commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 84 tasks before this scaffold; latest task ID was `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; local checkpoint selects this task. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | 13 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | 11 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Commands: status, validate, fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |
| local upgrade dry-run static report generator | PASS_WITH_WARNINGS | 3 upgrade scenarios checked; 1 missing static expected report ref; 0 defects. |

Post-change validation is recorded after final validation runs in this same file before commit.

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected task artifacts, upgrade dry-run reports, queue/context updates, and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged whitespace errors; nothing staged at the time. |
| `git diff --check HEAD^ HEAD` | PASS | Previous checkpoint commit still has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 85 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this task uses its local `next-batch.md` for safe next batch. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | Status `needs_review`; classification complete; 14 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` | PASS | 14 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 13 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | 13 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repository validation passed. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-upgrade status` | NOT_RUN | Command namespace is not implemented; CLI rejects `lifecycle-upgrade`. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-upgrade dry-run` | NOT_RUN | Command namespace is not implemented; CLI rejects `lifecycle-upgrade`. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-upgrade verify` | NOT_RUN | Command namespace is not implemented; CLI rejects `lifecycle-upgrade`. |
| JSON parse and no-apply proof check | PASS | Parsed 17 JSON files: upgrade dry-run reports, generated upgrade plans, static expected upgrade reports, scenario metadata, and plan index; no top-level no-apply booleans were enabled. |
| Boundary text search | PASS | 33 task/report files checked; required upgrade dry-run, no-apply, managed-section, hash, drift, review-gate, and prohibited-operation concepts are represented; no enabling markers found. |
| Secret scan over changed files | PASS | `rg --pcre2` over changed and untracked files found no credential-like assignments for secret/token/API key patterns. |
| YAML surface check | PASS_WITH_NOTES | Corrected structural check confirmed task ID, allowed paths, protected paths, forbidden operations, status, result, and review gate; full YAML parse not available because PyYAML is not installed. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | No Python implementation files changed in this task. |

Validation warning:

- An initial ad hoc YAML surface check expected `task_id` inside `task.yaml`; live queue convention uses `id`. The corrected structural check passed.
