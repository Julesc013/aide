# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01 - Explicit Fixture Apply Authority

## GOAL

Create a review-gated authority decision for exactly one future fixture-scoped managed-section apply attempt.

## WHY

The first fixture apply proof was blocked because the upstream gate selected the task but did not authorize execution. This task supplies the explicit authority decision without executing apply.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply-authority/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/**`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply-authority/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/**`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/**`

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
- generated lifecycle fixture plans
- expected lifecycle reports
- static fixture target files
- implementation files
- `core/**`

## IMPLEMENTATION

- Record authority disposition.
- Write authority packet and future apply contract.
- Do not execute apply in this task.
- Select `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01-RETRY`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply-authority/*.json`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply-authority/*.md`

## NON_GOALS

No fixture apply execution in this task, lifecycle apply, rollback execution, uninstall execution, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- JSON parse of authority packet and authority reports
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- scoped-transaction, managed-section, and transaction status
- boundary and secret scans
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Authority task exists and is indexed.
- Authority disposition is explicit.
- Authority packet exists and parses.
- Future apply contract exists.
- No apply-capable operation is executed by this task.

## OUTPUT_SCHEMA

Return the authority final report with disposition, files, validation, evidence, boundary review, warnings, risks, forbidden operations preserved, and next task.

## TOKEN_ESTIMATE

- approx_tokens: 1800
- budget_status: PASS
