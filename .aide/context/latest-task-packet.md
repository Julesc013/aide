# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01 - Lifecycle Fixture Upgrade Dry-Run Checks

## GOAL

Run report-only and dry-run upgrade planning checks against generated upgrade fixture plans and expected reports without implementing upgrade apply, executing upgrade apply, executing lifecycle apply, running scoped transaction apply against fixture targets, mutating fixture target files, mutating active AIDE repo files through scoped transaction apply, or mutating target repositories.

## WHY

`AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` accepted the install dry-run evidence with notes and selected this WorkUnit as the next smallest safe lifecycle planning surface before lifecycle repair dry-run or any future fixture apply gate.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/`
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

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/**`
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
- generated upgrade plans
- static fixture target files
- `core/**`

## REVIEW

- Review the three upgrade scenarios: `upgrade-v2`, `upgrade-manual-preserved`, and `drift-detected`.
- Verify generated plan reports, static expected reports where present, path boundaries, managed-section preservation, drift detection, hash references, no-apply proof, scoped executor interlock, and capability labels.
- Classify the missing static expected report ref for `upgrade-manual-preserved`.
- Produce upgrade dry-run reports and select the next safe checkpoint WorkUnit.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01` queue scaffold.
- Generate report-only upgrade dry-run evidence under `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`.
- Record result `PASS_WITH_WARNINGS` because `upgrade-manual-preserved` lacks a static expected report ref.
- Select `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01` as the next task-local safe WorkUnit.
- Do not repair generated upgrade plans or fixture files in this task.
- Do not implement or execute install apply, upgrade apply, lifecycle repair apply, rollback apply, uninstall apply, lifecycle apply, scoped transaction fixture apply, active repo apply, or target repo mutation.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/*.json`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/*.md`

## NON_GOALS

No install apply implementation or execution, upgrade apply implementation or execution, lifecycle repair apply implementation or execution, rollback implementation or execution, uninstall implementation or execution, lifecycle apply implementation or execution, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- upgrade dry-run report parse checks
- upgrade plan/expected report/scenario metadata parse checks
- no-apply proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Task exists and is indexed.
- All three upgrade scenarios are checked.
- Expected reports and generated plan reports are coherent where present.
- Missing static expected report ref for `upgrade-manual-preserved` is classified.
- Path boundaries, managed-section expectations, hash references, drift detection, no-apply flags, scoped executor interlock, and capability labels are reviewed.
- Status ends at `needs_review`.
- No upgrade apply, lifecycle apply, scoped transaction fixture apply, fixture target mutation, target mutation, branch/worktree mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1800
- budget_status: PASS
