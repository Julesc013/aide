# AIDE Latest Task Packet

## PHASE

AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning After Accepted Scoped Transaction Executor

## GOAL

Create a planning-only apply lifecycle plan after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was accepted with notes and Task OS current/latest reporting was repaired.

## WHY

The scoped executor is accepted with notes, but install, upgrade, lifecycle repair, rollback, uninstall, active repo apply, target repo adoption, branch/worktree mutation, release/promotion, provider/model calls, Gateway calls, network calls, and broad active-repo apply remain prohibited or deferred. A proof ladder is required before any fixture or apply-capable lifecycle task can be considered.

## CONTEXT_REFS

- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/queue/Q43-install-plan-model-v0/`
- `.aide/queue/Q44-repair-doctor-model-v0/`
- `.aide/queue/Q45-upgrade-model-v0/`
- `.aide/queue/Q46-rollback-uninstall-model-v0/`

## ALLOWED_PATHS

- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-command-status.md`
- `.aide/reports/task-os-next-plan.md`
- `.aide/reports/task-os-task-status.md`
- `README.md`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`
- `.env.*`
- `secrets/**`
- `credentials/**`
- target repositories
- release publication files
- provider/model/Gateway integration files
- branch/worktree automation files
- scoped transaction executor implementation files
- managed-section implementation files
- install/upgrade/repair/rollback/uninstall implementation files
- `.aide/install/**`
- `.aide/repair/**`
- `.aide/upgrade/**`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `core/**`
- `docs/reference/**`

## IMPLEMENTATION

- Create planning/report/evidence artifacts only.
- Define capability labels, proof ladder, blocked states, validation, evidence, and review gates.
- Select exactly one next WorkUnit without executing it.

## EVIDENCE

- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/lifecycle-plan.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/lifecycle-graph.json`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/next-batch.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/evidence/preconditions.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/evidence/capability-reality.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/evidence/validation.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/evidence/boundary-confirmation.md`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/evidence/remaining-risks.md`

## NON_GOALS

- No lifecycle apply execution.
- No install apply implementation or execution.
- No upgrade apply implementation or execution.
- No lifecycle repair apply implementation or execution.
- No rollback/uninstall implementation or execution.
- No active AIDE repo apply.
- No target repository mutation.
- No branch/worktree mutation, merge, push, promotion, tag, or release publication.
- No GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply.
- No production-ready or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-LIFECYCLE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-LIFECYCLE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- boundary text searches
- changed-file secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Lifecycle planning gate is recorded.
- Capability reality for lifecycle surfaces is honest and review-gated.
- Lifecycle proof ladder is ordered from schemas/fixtures before any apply.
- Selected next task is `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`.
- No lifecycle apply implementation or execution occurs.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return `STATUS`, `SUMMARY`, `FILES CHANGED`, `LIVE REPO STATE`, `LIFECYCLE PLANNING GATE`, `CAPABILITY REALITY`, `LIFECYCLE PROOF LADDER`, `VALIDATION`, `WARNINGS`, `FORBIDDEN OPERATIONS PRESERVED`, and `NEXT TASK`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1140
- budget_status: PASS
