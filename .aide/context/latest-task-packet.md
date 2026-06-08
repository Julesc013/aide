# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01 - Lifecycle Fixture Rollback Record Checkpoint

## GOAL

Independently review rollback-compatible lifecycle fixture record examples and rollback evidence before rollback dry-run, rollback execution, uninstall execution, fixture apply, active repo apply, or target repo apply gates.

## WHY

`AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` accepted repair dry-run evidence with notes and selected rollback record review as the next safety prerequisite before rollback dry-run or any fixture apply gate.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/`
- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/**`
- `.aide/examples/apply/lifecycle-fixtures/target/**`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/**`
- `core/apply/transaction_executor.py`
- `core/apply/tests/test_transaction_executor.py`
- `.aide/policies/scoped-transaction-executor.yaml`
- `docs/reference/apply-lifecycle-schemas.md`
- `docs/reference/scoped-transaction-executor.md`

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
- rollback record files
- generated lifecycle fixture plans
- static fixture target files
- `core/**`

## REVIEW

- Review rollback record schema alignment.
- Review generic and fixture rollback-compatible records.
- Verify generated plan and expected report rollback links.
- Verify preimage/postimage hash strategy and content references.
- Verify inverse-operation shape, rollback preconditions, rollback stop conditions, unsupported rollback cases, manual preservation, and protected-path handling.
- Verify scoped executor interlock and no-rollback-execution proof.
- Produce checkpoint disposition and next safe WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` queue scaffold.
- Record checkpoint disposition `ACCEPTED_WITH_NOTES`.
- Record that rollback-compatible records are static compatibility evidence only and do not authorize rollback execution.
- Select `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` as the next task-local safe WorkUnit.
- Do not repair rollback records, generated plans, expected reports, reports, fixture targets, or lifecycle code in this task.
- Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/evidence/*.md`

## NON_GOALS

No rollback apply implementation or execution, uninstall apply implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- rollback record schema parse
- rollback-compatible record parse
- generated plan and expected report rollback link checks
- no-rollback-execution proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Checkpoint task exists and is indexed.
- Rollback record schema and examples are independently reviewed.
- Fixture rollback records are coherent and linked from plans/reports.
- Preimage/postimage references, inverse operations, preconditions, stop conditions, manual preservation, protected paths, scoped executor interlock, and no-rollback-execution evidence are reviewed.
- Checkpoint disposition is explicit.
- Status ends at `needs_review`.
- No rollback apply, uninstall apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1800
- budget_status: PASS
