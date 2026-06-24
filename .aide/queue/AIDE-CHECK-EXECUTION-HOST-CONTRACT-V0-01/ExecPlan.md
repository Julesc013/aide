# AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01 ExecPlan

## Objective

Independently check the projection-only ExecutionHost contract v0 build without
repairing implementation.

## Scope

Allowed changes are limited to this check task packet, check reports, queue
index registration, and focused PLANS/IMPLEMENT entries.

Forbidden changes include production protocol files, schemas, tests, generated
build reports, core execution/provider code, interop adapters, hosts, and local
state.

## Current Facts

- Source build task: `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`.
- Source build commit: `4a1f1aa`.
- Source build result: `PASS_WITH_WARNINGS`.
- Source build recommends this check task.
- This check must recommend either `AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`
  or `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-REPAIR-01`.

## Milestones

- [x] Verify queue truth and source build status.
- [x] Inspect protocol helper, schema, CLI wiring, tests, and generated reports.
- [x] Run independent task-local harness.
- [x] Run focused validation matrix and leakage scans.
- [x] Write final check result and commit.

## Validation

Run the independent harness, focused ExecutionHost tests, AIDE Lite
execution-host commands, task inspect/evidence, broad validation, leak scans,
diff checks, and commit policy.

## Recovery

If interrupted, inspect `git status --short --branch`, run the harness at
`.aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01/evidence/check_execution_host_contract.py`,
then continue from the latest incomplete evidence entry.

## Exit

Stop at `needs_review`. If no material findings remain, record
`PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, and
recommend exactly `AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`.
