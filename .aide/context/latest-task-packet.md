# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01 - Lifecycle Fixture Repair Dry-Run Checkpoint

## GOAL

Independently review and checkpoint `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` without implementing or executing lifecycle repair apply, lifecycle apply, scoped transaction fixture apply, active repo apply, or target repo mutation.

## WHY

`AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` completed as a report-only dry-run WorkUnit with warnings and selected this checkpoint as the next safe task. The checkpoint determines whether the repair dry-run evidence is accepted with notes, needs repair, is rejected, or is blocked before rollback record review or later lifecycle fixture work.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-repair-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-missing-marker/README.md`
- `.aide/examples/apply/lifecycle-fixtures/expected/repair-plan-malformed-marker/README.md`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-repair-dry-run/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/**`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/examples/apply/lifecycle/**`
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
- generated repair plans
- static fixture target files
- `core/**`

## REVIEW

- Review repair scenarios `repair-plan-missing-marker` and `repair-plan-malformed-marker`.
- Verify generated repair plans, generated plan reports, expected-state README fallback evidence, missing static expected repair report refs, path boundaries, managed-section marker expectations, hash references, drift context, no-apply proof, scoped executor interlock, and capability labels.
- Classify absent static expected repair report refs for both repair scenarios.
- Produce checkpoint disposition and next safe WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01` queue scaffold.
- Record checkpoint disposition `ACCEPTED_WITH_NOTES`.
- Record that static expected repair report refs are absent and non-blocking for this checkpoint.
- Select `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` as the next task-local safe WorkUnit.
- Do not repair generated repair plans, expected report fixtures, reports, or lifecycle code in this task.
- Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-repair-dry-run/*.json`
- `.aide/reports/lifecycle-fixture-repair-dry-run/*.md`

## NON_GOALS

No install apply implementation or execution, upgrade apply implementation or execution, lifecycle repair apply implementation or execution, rollback implementation or execution, uninstall implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- repair dry-run report parse checks
- generated repair plan parse checks
- generated repair plan report parse checks
- expected-state README fallback evidence checks
- scenario metadata parse checks
- no-apply proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Checkpoint task exists and is indexed.
- Both repair scenarios are independently reviewed.
- Generated repair plans and generated plan reports match fixture metadata.
- Missing marker and malformed marker expectations are verified.
- Expected repair report refs are classified.
- Path boundaries, managed-section marker behavior, hash references, drift evidence, no-apply flags, scoped executor interlock, and capability labels are reviewed.
- Checkpoint disposition is explicit.
- Status ends at `needs_review`.
- No lifecycle repair apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1800
- budget_status: PASS
