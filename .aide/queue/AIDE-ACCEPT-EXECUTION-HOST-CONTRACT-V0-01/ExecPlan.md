# AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01 ExecPlan

## Objective

Accept only the projection-only `execution_host_contract_v0` capability after
the build and check gates passed with warnings and zero material findings.

## Scope

Allowed changes are limited to this acceptance task packet, acceptance reports,
queue index registration, and focused PLANS/IMPLEMENT entries.

This acceptance does not modify production code, schemas, tests, build reports,
check reports, provider code, interop adapters, hosts, or local state.

## Current Facts

- Build task: `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`.
- Build result: `PASS_WITH_WARNINGS`, missing evidence `0`.
- Check task: `AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`.
- Check result: `PASS_WITH_WARNINGS`, material findings `0`, missing evidence `0`.
- Next task after acceptance must be
  `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

## Milestones

- [x] Verify build and check gate evidence.
- [x] Record accepted capability boundary.
- [x] Preserve warnings and explicit non-capabilities.
- [x] Write acceptance reports and task evidence.
- [x] Run final validation and commit checks.

## Validation

Run task inspect/evidence, broad validation, path and secret scans, diff checks,
and commit policy. Focused ExecutionHost validation may be rerun as supporting
evidence, but this acceptance must not repair implementation.

## Recovery

If interrupted, inspect `git status --short --branch`, rerun task
inspect/evidence for this acceptance task, then continue from the latest
incomplete evidence entry.

## Exit

Stop at `needs_review` with `ACCEPTED_WITH_WARNINGS`, accepted capability
exactly `execution_host_contract_v0`, missing evidence `0`, and recommended
next task exactly `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.
