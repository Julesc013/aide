# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01 - Blocked First Fixture Apply Proof

## GOAL

Evaluate the first fixture-scoped managed-section apply proof against live authority and stop safely if the required mutation authority is absent.

## WHY

The attached mutation proof pack requires explicit live gate authority before executing the first fixture apply. The live apply gate selected this task but records `apply_authorized_by_this_gate: false`.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/`
- `.aide/reports/lifecycle-fixture-apply-gate/gate-decision.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/**`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/**`
- `.aide/reports/lifecycle-fixture-apply-gate/**`
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

- Record blocked authority state.
- Do not execute dry-run/apply.
- Do not mutate fixture targets.
- Select an explicit authority WorkUnit as the next safe task.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply/*.json`
- `.aide/reports/lifecycle-fixture-install-managed-section-apply/*.md`

## NON_GOALS

No fixture apply execution, lifecycle apply, scoped transaction fixture apply, rollback execution, uninstall execution, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- JSON parse of blocker report
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- boundary and secret scans
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Blocked task exists and is indexed.
- Blocker is explicit and evidence-backed.
- No fixture target is mutated.
- No apply-capable operation is executed.

## OUTPUT_SCHEMA

Return the standard AIDE final report with summary, files, validation, unresolved warnings, and forbidden-operation confirmation.

## TOKEN_ESTIMATE

- approx_tokens: 1600
- budget_status: PASS
