# Validation

Pre-check commands:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial status was clean on `main...origin/main`. |
| `git remote -v` | PASS | `origin` fetch/push configured. |
| `git rev-parse HEAD` | PASS | Initial HEAD `2d7ebb7f53d056ac0fcafebee18ffc12d072b872`. |
| `git show --stat --oneline --name-status HEAD` | PASS | Latest commit is the install dry-run WorkUnit checkpoint. |
| `git diff --check HEAD^ HEAD` | PASS | No whitespace errors in latest commit. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 83 tasks before this checkpoint was created; latest task ID was `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | PASS | Classification complete, evidence files 12, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` | PASS | 12 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | NOT_RUN | Positional form is unsupported by current CLI; command exits with unrecognized arguments. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | Classification complete, evidence files 11, missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` | PASS | 11 evidence files listed, missing none. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only, no lifecycle apply or target mutation. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks, fixture shape only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Full repo validation passed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema --help` | PASS | Commands: status, validate, fixture-verify. |
| `py -3 .aide/scripts/aide_lite.py task --help` | PASS | Task inspect/evidence require subcommand options. |
| independent install dry-run JSON review | PASS_WITH_WARNINGS | 5 install scenarios checked; 3 static expected reports present; 2 missing static expected report refs; 0 defects. |

Post-change validation:

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS_WITH_CHANGES | Expected checkpoint artifacts and deterministic report refreshes only. |
| `git diff --check` | PASS | No whitespace errors in working-tree diff. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | Status `needs_review`; classification complete; 13 evidence files; missing evidence 0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` | PASS | 13 evidence files listed; missing none. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | 84 tasks; latest task ID is `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`. |
| `py -3 .aide/scripts/aide_lite.py task next-plan` | PASS_WITH_NOTES | Global selector still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`; this checkpoint uses local `next-batch.md` for the selected next WorkUnit. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema status` | PASS | Report-only; no lifecycle apply, target mutation, branch mutation, provider/model calls, Gateway calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate` | PASS | 280 checks; dry-run/report-only; production-ready false and release-ready false. |
| `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify` | PASS | 298 checks; fixture shape only; lifecycle apply not executed. |
| `py -3 .aide/scripts/aide_lite.py scoped-transaction status` | PASS | Target repo capable false; broad active repo apply false; production-ready false; release-ready false. |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS | Active repo apply false; real repo apply allowed false. |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS | Report-only; real repo apply allowed false; fixture-only transaction planning true. |
| JSON and structural YAML surface checks | PASS_WITH_NOTES | Parsed 22 JSON files; structurally checked 3 YAML surfaces because PyYAML is unavailable. |
| No-apply proof check | PASS | 8 install dry-run reports checked; top-level mutation and apply-execution booleans remain false. |
| Boundary text search | PASS | Required checkpoint, install dry-run, no-apply, protected-path, managed-section, hash, review-gate, and prohibited-operation concepts are represented; no top-level enabling booleans found. |
| Secret scan over changed and reviewed files | PASS | `rg --pcre2` over 49 files found no credential-like assignments for secret/token/API key patterns. |
| `py -3 .aide/scripts/aide_lite.py validate` | FAIL_THEN_PASS | First post-change run failed because latest task packet lacked `IMPLEMENTATION`; fixed inside allowed path, then rerun passed. |

Validation warning:

- Missing static expected report refs for `install-clean` and `install-existing-manual-preserved` are non-blocking for this checkpoint but remain an evidence-completeness gap.
