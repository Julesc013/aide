# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01 - Generate No-Apply Lifecycle Fixture Plans

## GOAL

Generate deterministic dry-run/report-only lifecycle fixture plans from reviewed static fixture metadata, expected reports, rollback records, and lifecycle plan schema.

## WHY

`AIDE-LIFECYCLE-FIXTURE-CHECK-01` accepted static lifecycle fixtures with notes and selected this WorkUnit as the next safe batch before any dry-run execution or apply authority is considered.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/reports/lifecycle-schema-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/source-pack/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/**`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/**`
- `.aide/apply/lifecycle-*.schema.json`

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

- Create the `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01` queue scaffold.
- Generate 13 no-apply lifecycle fixture plan JSON files.
- Generate a plan index and lifecycle fixture plan reports.
- Record scenario matrix, validation, no-apply proof, scoped executor interlock, capability reality, and next batch.
- Do not implement a generator CLI command in this task.
- Stop at `needs_review`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/evidence/*.md`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/plan-index.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/*.plan.json`
- `.aide/reports/lifecycle-fixture-plans/*`

## NON_GOALS

- No generator CLI/source implementation, fixture repair, lifecycle apply implementation/execution, scoped transaction fixture apply, active repo apply, install/upgrade/repair/rollback/uninstall apply, rollback apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- generated plan parse/structural checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Plan-generator queue scaffold exists and is indexed.
- 13 generated plans exist with 13/13 scenario coverage.
- Plan index and plan-generation reports exist.
- Generated plans parse and satisfy required lifecycle plan fields.
- Generated plans preserve no-mutation/no-apply false flags.
- Status ends at `needs_review`.
- No forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1320
- budget_status: PASS
