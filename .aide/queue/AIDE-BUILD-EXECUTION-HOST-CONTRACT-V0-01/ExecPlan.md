# AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01 ExecPlan

## Objective

Build the provider-neutral ExecutionHost contract v0 as projection-only protocol
work.

## Scope

Allowed implementation is limited to:

- `core/protocol/execution_host.py`
- `.aide/protocol/aide-execution-host.schema.json`
- AIDE Lite status/project/validate command wiring
- focused tests
- generated reports and task evidence

No live host, local process host, worker execution, scheduler, service,
transport, provider/model/network call, preview/apply, repository mutation, or
branch/GitHub/release behavior is authorized.

## Current Facts

- `registered_process_execution_provider_v0` is accepted with warnings.
- Deterministic capability execution and worker/session execution must remain
  distinct.
- The next task after this build must be
  `AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`.

## Milestones

- [x] Inspect existing protocol/report patterns.
- [x] Add projection-only helper and schema.
- [x] Wire AIDE Lite `execution-host` status/project/validate.
- [x] Add focused tests.
- [x] Generate reports and task evidence.
- [x] Run final validation and commit checks.

## Validation

Run focused tests, command status/project/validate, task inspect/evidence,
broad validation, leak scans, diff checks, and commit policy.

## Recovery

If interrupted, inspect `git status --short --branch`, rerun
`py -3 .aide/scripts/aide_lite.py execution-host validate`, then continue from
the latest incomplete evidence entry.

## Exit

Stop at `needs_review` with `PASS_WITH_WARNINGS`, missing evidence `0`, and
recommended next task exactly `AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`.
