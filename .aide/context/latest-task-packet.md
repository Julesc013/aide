# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01 - Lifecycle Fixture Rollback Dry-Run Checkpoint

## GOAL

Independently review and checkpoint `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` and its report-only rollback dry-run evidence.

## WHY

`AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01` completed rollback dry-run checks with `PASS_WITH_WARNINGS` and selected this WorkUnit as the smallest safe independent checkpoint before uninstall dry-run, rollback execution, fixture apply, active repo apply, or target repo adoption gates.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-rollback-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-rollback-dry-run/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/**`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/**`
- `.aide/examples/apply/lifecycle-fixtures/target/**`
- `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/apply/lifecycle-*.schema.json`
- `docs/reference/apply-lifecycle-schemas.md`
- `core/apply/transaction_executor.py`
- `.aide/policies/scoped-transaction-executor.yaml`
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
- expected lifecycle reports
- static fixture target files
- `core/**`

## REVIEW

- Verify rollback dry-run reports.
- Verify rollback record consumption.
- Verify current-hash checks and placeholder classifications.
- Verify inverse operation checks.
- Verify rollback preconditions and stop conditions.
- Verify manual preservation and protected path handling.
- Verify scoped executor interlock and no-rollback-execution proof.
- Verify capability labels and validation evidence.
- Produce checkpoint evidence and select the next safe WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01` queue scaffold.
- Review deterministic report-only rollback dry-run evidence.
- Accept the rollback dry-run evidence with notes if coherent.
- Select `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` as the next task-local safe WorkUnit if accepted.
- Do not repair rollback dry-run reports, rollback records, generated plans, expected reports, fixture targets, lifecycle code, scoped transaction executor code, or managed-section implementation in this task.
- Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/evidence/*.md`

## NON_GOALS

No rollback apply implementation or execution, uninstall apply implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- rollback dry-run report JSON parse
- no-rollback-execution proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Rollback dry-run checkpoint task exists and is indexed.
- Checkpoint disposition is explicit.
- Rollback dry-run reports parse and are reviewed.
- Current-hash, inverse-operation, precondition, stop-condition, manual-preservation, protected-path, scoped-executor-interlock, no-rollback-execution, and capability label checks are recorded.
- Status ends at `needs_review`.
- No rollback apply, uninstall apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1700
- budget_status: PASS
