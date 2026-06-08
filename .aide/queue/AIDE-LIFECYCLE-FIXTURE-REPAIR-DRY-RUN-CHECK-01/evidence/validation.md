# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`; subsequent preflight AIDE status commands refreshed deterministic reports. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `6eddb33c8c0c1431ea0d4a5bb2c94afe92b6bcd5`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the repair dry-run WorkUnit. |
| `git diff --check HEAD^ HEAD` | PASS | Latest repair dry-run commit has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 87 tasks; latest task ID was `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | Status `needs_review`; classification complete; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | 16 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Available lifecycle-schema subcommands are status, validate, and fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require `--task-id`. |
| Independent repair dry-run static review | PASS_WITH_WARNINGS | 2 repair scenarios checked; 2 missing static expected repair report refs; 0 defects. |

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected checkpoint artifacts, queue/context updates, and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged whitespace errors; nothing staged at the time. |
| `git diff --check HEAD^ HEAD` | PASS | Previous repair dry-run commit has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 88 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this checkpoint uses local `next-batch.md`. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 15 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | Status `needs_review`; classification complete; 16 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` | PASS | 16 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 15 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` | PASS | 15 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS_WITH_WARNINGS | Full validation passed; known warning remains `compact task packet over target: 1951 > 1800`, while latest task packet passed at 1951 tokens. |
| JSON parse and YAML surface check | PASS | Parsed 15 JSON files: repair dry-run reports, generated repair plans, generated plan reports, and scenario metadata; task/status YAML surfaces include required checkpoint fields. |
| Independent repair dry-run consistency check | PASS | 2 scenarios, 0 expected static report refs, 2 hash matches, 2 marker checks, no apply evidence. |
| Boundary text search | PASS | 27 terms checked across checkpoint files and repair dry-run reports; required concepts are represented as blocked, deferred, review-only, or prohibited. |
| Secret scan over changed files | PASS | 43 changed files scanned with 10 credential-marker assignment patterns; no matches. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | No Python implementation files changed in this checkpoint. |

Validation warning:

- Initial boundary text search missed exact spaced terms `managed section`, `missing marker`, and `malformed marker`; boundary evidence wording was updated and the corrected boundary search passed.
