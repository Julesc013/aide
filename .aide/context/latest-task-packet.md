# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01 - Lifecycle Expected Report Gap Repair

## GOAL

Add static expected report files for the six lifecycle fixture expected-report gaps identified by proof closure.

## WHY

`AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01` closed the dry-run proof ladder with `PASS_WITH_WARNINGS` and selected this repair before fixture apply gate planning.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/`
- `.aide/reports/lifecycle-expected-report-gap-repair/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/`
- `.aide/reports/lifecycle-fixture-proof-closure/`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/`
- `.aide/reports/lifecycle-fixture-plans/`
- `.aide/examples/apply/lifecycle-fixtures/expected/`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/**`
- `.aide/reports/lifecycle-expected-report-gap-repair/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-clean.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-existing-manual-preserved.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/upgrade-manual-preserved.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/repair-plan-missing-marker.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/repair-plan-malformed-marker.report.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/uninstall-manual-preserved.report.json`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/**`
- `.aide/reports/lifecycle-fixture-proof-closure/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/**`
- `.aide/examples/apply/lifecycle-fixtures/target/**`

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
- static fixture target files
- implementation files
- `core/**`

## IMPLEMENTATION

- Add six static expected report files.
- Add repair summary reports and queue evidence.
- Do not update generated plans in this WorkUnit.
- Select `AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01` if static expected-report file coverage is complete.

## NON_GOALS

No generated plan mutation, fixture target mutation, fixture apply gate execution, fixture apply execution, lifecycle apply, rollback execution, uninstall execution, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, production-ready claim, or release-ready claim.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01/evidence/*.md`
- `.aide/reports/lifecycle-expected-report-gap-repair/*.json`
- `.aide/reports/lifecycle-expected-report-gap-repair/*.md`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/*.report.json`

## VALIDATION

- git status/diff checks
- JSON parse of new expected reports and repair reports
- expected-report inventory check
- hash spot checks
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- boundary and secret scans
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Six expected report files exist and parse.
- Repair summary exists and parses.
- Queue task is indexed and complete.
- No generated plans or fixture targets are mutated.
- No apply-capable operation is authorized or executed.

## OUTPUT_SCHEMA

Return the standard AIDE final report with summary, files, validation, unresolved warnings, and forbidden-operation confirmation.

## TOKEN_ESTIMATE

- approx_tokens: 1700
- budget_status: PASS
