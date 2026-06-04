# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01 - Lifecycle Schemas and Fixture Plan

## GOAL

Define lifecycle manifest, lifecycle plan, lifecycle report, rollback-compatible lifecycle record, and fixture repository shape needed before any install, upgrade, lifecycle repair, rollback, or uninstall apply proof.

## WHY

`AIDE-APPLY-LIFECYCLE-PLAN-01` selected this task as the next safe WorkUnit after the scoped transaction executor was accepted with notes. Lifecycle schemas and fixture shape must exist before any fixture lifecycle proof can be proposed. This task remains schema, example, fixture-shape, documentation, and evidence work only.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/queue/AIDE-TASK-OS-STATUS-REPAIR-01/`
- `.aide/queue/Q43-install-plan-model-v0/`
- `.aide/queue/Q44-repair-doctor-model-v0/`
- `.aide/queue/Q45-upgrade-model-v0/`
- `.aide/queue/Q46-rollback-uninstall-model-v0/`
- `docs/reference/apply-lifecycle-schemas.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/apply/lifecycle-manifest.schema.json`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/apply/lifecycle-report.schema.json`
- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/examples/apply/lifecycle/**`
- `docs/reference/apply-lifecycle-schemas.md`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `.aide/reports/scoped-transaction-executor-*.md`
- `.aide/reports/scoped-transaction-executor-*.json`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`
- `.aide/reports/current-aide-roadmap.md`
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
- unrelated docs/reference files
- release roots

## IMPLEMENTATION

- Create lifecycle schema, example, fixture-shape, documentation, queue, status, and evidence artifacts only.
- Define artifact model, schema summaries, rollback-compatible record shape, scoped executor interlock, minimal validation design, and token/quality ledger hook.
- Select exactly one next WorkUnit without executing it.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/schema-plan.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/fixture-plan.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/rollback-record-plan.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/lifecycle-fixture-graph.json`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/next-batch.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/preconditions.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/schema-summary.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/fixture-summary.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/validation.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/boundary-confirmation.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/evidence/remaining-risks.md`

## NON_GOALS

- No lifecycle apply implementation or execution.
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
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- parse lifecycle fixture graph JSON
- parse changed JSON and YAML files
- boundary text searches
- changed-file secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Lifecycle schema and fixture planning task scaffold exists.
- Lifecycle manifest, plan, report, and rollback-compatible record schemas exist.
- Lifecycle examples exist and remain non-mutating.
- Fixture repository shape is defined but fixture materialization is deferred.
- Rollback-compatible record shape is defined without rollback execution.
- Scoped transaction executor v0 interlock and limitations are explicit.
- Selected next task is `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return `STATUS`, `SUMMARY`, `FILES CHANGED`, `LIVE REPO STATE`, `PRECONDITIONS`, `ARTIFACT MODEL`, `SCHEMA PLAN`, `FIXTURE PLAN`, `ROLLBACK-COMPATIBLE RECORD`, `SCOPED EXECUTOR INTERLOCK`, `TOKEN/QUALITY LEDGER HOOK`, `SAFE NEXT BATCH`, `VALIDATION`, `EVIDENCE`, `BOUNDARY REVIEW`, `WARNINGS`, `UNRESOLVED RISKS`, `FORBIDDEN OPERATIONS PRESERVED`, and `NEXT TASK`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1700
- budget_status: PASS
