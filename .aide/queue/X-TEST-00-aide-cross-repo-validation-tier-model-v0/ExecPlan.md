# X-TEST-00 ExecPlan

## Objective

Implement the first portable AIDE validation tier and test telemetry contract model.

## Scope

Write only the X-TEST-00 queue packet, portable AIDE policy/schema/template/docs, AIDE Lite report-only command support, tests, golden tasks, compact reports, generated `.aide/tests/latest-*` artifacts, the export pack, and compact task/review packets. Dominium and Eureka remain read-only and target test suites are not run.

## Plan

- [x] Confirm AIDE repository identity and baseline state.
- [x] Inspect XCHECK-01R evidence.
- [x] Run baseline validation and record the pre-existing review-packet token warning.
- [x] Add portable validation tier, impacted-test, telemetry, handoff, summary, and promotion policies.
- [x] Add schemas, examples, docs, golden tasks, and unit tests.
- [x] Extend AIDE Lite with report-only `test` subcommands while preserving `test`.
- [x] Generate `.aide/tests/latest-*` reports and X-TEST-00 compact reports.
- [x] Regenerate export pack and X-TEST-01 task packet.
- [x] Run final validation with no warnings.
- [x] Commit scoped changes.

## Verification Intent

Run targeted syntax/unit checks first, then AIDE Lite command checks, then broader AIDE validation and export-pack validation. The full target suites for Dominium and Eureka are deliberately not run.

## Blockers

None. The baseline review-packet token warning and generated-manifest warning were cleared before final status.
