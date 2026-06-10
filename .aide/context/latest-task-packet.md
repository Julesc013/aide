# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01 - Lifecycle Fixture Apply Gate

## GOAL

Create a planning-only fixture apply gate and select the smallest safe future fixture apply candidate.

## WHY

The lifecycle dry-run proof ladder is closed, expected-report file gaps have been repaired, and the next safe step is a gate decision, not apply execution.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/`
- `.aide/reports/lifecycle-fixture-apply-gate/`
- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/`
- `.aide/queue/AIDE-APPLY-02-REPAIR-01/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/`
- `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/**`
- `.aide/reports/lifecycle-fixture-apply-gate/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-APPLY-02-REPAIR-01/**`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/**`
- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/**`
- `.aide/reports/lifecycle-fixture-proof-closure/**`
- `.aide/reports/lifecycle-expected-report-gap-repair/**`
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

- Record a gate decision.
- Select exactly one future fixture apply candidate.
- Do not execute fixture apply.
- Do not authorize fixture apply in this task.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-apply-gate/*.json`
- `.aide/reports/lifecycle-fixture-apply-gate/*.md`

## NON_GOALS

No fixture apply execution, lifecycle apply, scoped transaction fixture apply, rollback execution, uninstall execution, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- JSON parse of gate reports
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`
- scoped-transaction, managed-section, and transaction status checks where available
- `py -3 .aide/scripts/aide_lite.py validate`
- boundary and secret scans
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Gate task exists and is indexed.
- Gate report exists and parses.
- First future fixture apply candidate is explicit.
- Status ends at `needs_review`.
- No apply-capable operation is authorized or executed.

## OUTPUT_SCHEMA

Return the standard AIDE final report with summary, files, validation, unresolved warnings, and forbidden-operation confirmation.

## TOKEN_ESTIMATE

- approx_tokens: 1600
- budget_status: PASS
