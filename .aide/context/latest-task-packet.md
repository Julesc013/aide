# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01 - Lifecycle Fixture Uninstall Dry-Run Checks

## GOAL

Run report-only and dry-run uninstall planning checks against generated lifecycle fixture uninstall plans and expected evidence.

## WHY

`AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01` accepted rollback dry-run evidence with notes and selected this WorkUnit as the next missing lifecycle dry-run proof before proof closure, fixture apply, active repo apply, or target repo adoption gates.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-uninstall-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/uninstall-manual-preserved.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/broad-delete-blocked.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/broad-delete-blocked.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected/uninstall-manual-preserved/`
- `.aide/examples/apply/lifecycle-fixtures/expected/broad-delete-blocked/`
- `.aide/examples/apply/lifecycle-fixtures/target/uninstall-owned-and-manual/`
- `.aide/examples/apply/lifecycle-fixtures/target/broad-delete-attempt/`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-uninstall-dry-run/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/uninstall-manual-preserved.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/broad-delete-blocked.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/broad-delete-blocked.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected/uninstall-manual-preserved/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/broad-delete-blocked/**`
- `.aide/examples/apply/lifecycle-fixtures/target/uninstall-owned-and-manual/**`
- `.aide/examples/apply/lifecycle-fixtures/target/broad-delete-attempt/**`
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

- Verify generated uninstall plans and plan reports.
- Verify expected state and available expected reports.
- Verify manual preservation and broad-delete blocking.
- Verify protected path handling.
- Verify scoped executor interlock and no-uninstall-execution proof.
- Verify capability labels and validation evidence.
- Produce evidence and select the next safe WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01` queue scaffold.
- Create deterministic report-only uninstall dry-run reports.
- Classify missing static expected report refs.
- Select `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01` as the next task-local safe WorkUnit if successful.
- Do not repair uninstall plans, expected reports, fixture targets, lifecycle code, scoped transaction executor code, or managed-section implementation in this task.
- Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-uninstall-dry-run/*`

## NON_GOALS

No rollback apply implementation or execution, uninstall apply implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- uninstall dry-run report JSON parse
- no-uninstall-execution proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Uninstall dry-run task exists and is indexed.
- Uninstall dry-run reports exist and parse.
- Manual-preservation, broad-delete-blocking, protected-path, scoped-executor-interlock, no-uninstall-execution, and capability label checks are recorded.
- Status ends at `needs_review`.
- No uninstall apply, rollback apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1700
- budget_status: PASS
