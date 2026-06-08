# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01 - Generated Lifecycle Fixture Plan Checkpoint

## GOAL

Independently review and checkpoint `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` as a no-apply generated plan review before any future dry-run execution or apply widening.

## WHY

`AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` selected this checkpoint as the next safe batch after generating 13 deterministic lifecycle fixture plan artifacts and reports.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/reports/lifecycle-schema-*`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/status.yaml`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/review.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/examples/apply/lifecycle/**`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- release roots
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply and install/upgrade/repair/rollback/uninstall implementation files
- scoped transaction executor and managed-section implementation files
- `core/**`

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` queue checkpoint scaffold.
- Review generated plan index, 13 generated plans, 13 plan reports, scenario metadata, expected reports, rollback references, no-apply proof, scoped executor interlock, and capability labels.
- Record checkpoint disposition `ACCEPTED_WITH_NOTES`.
- Do not modify generated plan files.
- Stop at `needs_review`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/evidence/*.md`

## NON_GOALS

No generated-plan repair, lifecycle apply implementation or execution, scoped transaction fixture apply, active repo apply, install/upgrade/repair/rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- generated plan parse/structural checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Checkpoint queue scaffold exists and is indexed.
- 13 generated plans are reviewed and coherent.
- Plan index, plan reports, expected report links, rollback references, blocker labels, mutation-state fields, scoped executor interlock, and capability labels are reviewed.
- Status ends at `needs_review`.
- No generated plan repair or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1450
- budget_status: PASS
