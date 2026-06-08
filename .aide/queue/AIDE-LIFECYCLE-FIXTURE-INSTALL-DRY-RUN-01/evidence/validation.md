# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `0c2761bc21a14671155ccd28a80a1fbfc7e37494`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the generated lifecycle fixture plan checkpoint. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in latest commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 82 tasks; latest task ID was `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | 11 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | Classification complete, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` | PASS | 9 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Commands: status, validate, fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |
| local install dry-run static report generator | PASS_WITH_WARNINGS | 5 install scenarios checked; 2 missing static expected report refs; 0 defects. |

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected task artifacts and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `git diff --cached --check` | PASS | No staged whitespace errors; nothing staged at the time. |
| `git diff --check HEAD^ HEAD` | PASS | Previous checkpoint commit still has no whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 83 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this task uses its local `next-batch.md` for safe next batch. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | PASS | Status `needs_review`; classification complete; 12 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | PASS | 12 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repository validation passed. |
| JSON parse and no-apply proof check | PASS | Parsed 16 JSON files: 8 task reports, 5 generated install plans, and 3 static expected reports; no top-level no-apply booleans were enabled. |
| YAML surface check | PASS_WITH_NOTES | Structural check confirmed task ID, allowed paths, protected paths, forbidden operations, status, result, and review gate; full YAML parse not available because PyYAML is not installed. |
| Boundary text search | PASS | Required install dry-run, no-apply, protected-path, managed-section, hash, review-gate, and prohibited-operation concepts are represented; no top-level enabling booleans found in generated reports. |
| Secret scan over changed files | PASS | `rg --pcre2` over 47 changed files found no credential-like assignments for secret/token/API key patterns. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-install status` | NOT_RUN | Command namespace is not implemented; CLI rejects `lifecycle-install`. |
| `py -3 .aide/scripts/aide_lite.py install --help` | PASS | Install command group exists, but install status/dry-run commands were not run because this WorkUnit does not authorize `.aide/install/**` report churn or install planning execution. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | NOT_RUN | No Python implementation files changed in this task. |

Validation warning:

- An initial ad hoc JSON no-apply assertion expected proof fields under a nested `no_apply_proof` key and failed. The report schema stores those fields at top level; the corrected JSON parse/no-apply proof check passed.
