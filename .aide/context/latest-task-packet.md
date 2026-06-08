# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01 - Lifecycle Fixture Install Dry-Run Checkpoint

## GOAL

Independently review and checkpoint `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` without implementing install apply, executing install apply, executing lifecycle apply, running scoped transaction apply against fixture targets, mutating fixture target files, mutating active AIDE repo files through scoped transaction apply, or mutating target repositories.

## WHY

`AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` completed report-only install dry-run checks with warnings and selected this checkpoint as the next safe WorkUnit before moving to any upgrade dry-run or fixture apply gate.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-install-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-install-dry-run/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
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
- generated install plans
- static fixture target files
- `core/**`

## REVIEW

- Review the install dry-run WorkUnit and evidence.
- Review the five install scenarios: `install-clean`, `install-existing-manual-preserved`, `install-managed-section`, `protected-path-blocked`, and `traversal-blocked`.
- Verify generated plan reports, static expected reports where present, path boundaries, managed-section preservation, hash references, no-apply proof, scoped executor interlock, and capability labels.
- Classify missing static expected report refs for `install-clean` and `install-existing-manual-preserved`.
- Produce checkpoint disposition and next safe WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` queue scaffold.
- Independently review `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`.
- Record checkpoint disposition `ACCEPTED_WITH_NOTES`.
- Record that missing static expected report refs are non-blocking for this checkpoint.
- Select `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` as the next task-local safe WorkUnit.
- Do not repair install dry-run reports or generated install plans in this checkpoint.
- Do not implement or execute install apply, lifecycle apply, scoped transaction fixture apply, active repo apply, or target repo mutation.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/evidence/*.md`

## NON_GOALS

No install apply implementation or execution, upgrade apply implementation or execution, lifecycle repair apply implementation or execution, rollback implementation or execution, uninstall implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- install dry-run report parse checks
- install plan/expected report/scenario metadata parse checks
- no-apply proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Checkpoint task exists and is indexed.
- All five install scenarios are reviewed.
- Expected reports and generated plan reports are coherent.
- Missing static expected report refs are classified.
- Path boundaries, managed-section expectations, hash references, no-apply flags, scoped executor interlock, and capability labels are reviewed.
- Status ends at `needs_review`.
- No install apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1600
- budget_status: PASS
