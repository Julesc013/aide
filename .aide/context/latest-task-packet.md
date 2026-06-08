# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01 - Lifecycle Fixture Install Dry-Run Checks

## GOAL

Run report-only and dry-run install planning checks against generated install lifecycle fixture plans and expected reports without executing install apply, lifecycle apply, scoped transaction fixture apply, active repo apply, or target repo mutation.

## WHY

`AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01` accepted the generated lifecycle fixture plans with notes and selected install dry-run checking as the next smallest safe WorkUnit before any broader dry-run harness or apply gate.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/`
- `.aide/reports/lifecycle-fixture-install-dry-run/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- `.aide/reports/lifecycle-schema-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-install-dry-run/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

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
- `core/**`

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01` queue scaffold.
- Generate deterministic report-only install dry-run check reports.
- Check install scenarios only: `install-clean`, `install-existing-manual-preserved`, `install-managed-section`, `protected-path-blocked`, and `traversal-blocked`.
- Record expected report warnings, path boundaries, managed-section checks, hash checks, no-apply proof, capability reality, and next batch.
- Do not implement a `lifecycle-install` command in this task.
- Stop at `needs_review`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-install-dry-run/*`

## NON_GOALS

No install apply implementation or execution, lifecycle apply implementation or execution, scoped transaction fixture apply, active repo apply, upgrade/repair/rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PLAN-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- install dry-run report parse checks
- install plan/expected report/scenario metadata parse checks
- no-apply proof checks
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Install dry-run queue scaffold exists and is indexed.
- 5 install scenarios are checked.
- Expected reports and generated plan reports are checked.
- Path boundaries, managed-section expectations, hash references, no-apply flags, scoped executor interlock, and capability labels are checked.
- Status ends at `needs_review`.
- No install apply, lifecycle apply, scoped transaction fixture apply, target mutation, or forbidden operation is performed.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1500
- budget_status: PASS
