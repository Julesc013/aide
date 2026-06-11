# ExecPlan

## Objective

Independently check the lifecycle fixture temp runner implemented by
`AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01` and commit `04b6b6c`.

## Scope

This is a check-only task. It may create check WorkUnit artifacts, check
reports, and validation evidence. It may rerun the existing lifecycle fixture
runner, which writes under `.aide/reports/lifecycle-fixture-runner/**`.

## Non-Goals

- No implementation feature work.
- No service, Commander, provider adapter, branch/worktree, release, GitHub,
  Gateway, network, or model/provider work.
- No target repo apply, active repo apply, rollback execution, uninstall
  execution, or broad lifecycle apply.

## Allowed Paths

The allowlist is recorded in `task.yaml`. The check may write only the check
queue packet, check reports, `.aide/reports/lifecycle-fixture-runner/**`
runner validation outputs, `.aide/tmp/lifecycle-fixture-runs/**` if needed,
and `.aide/queue/index.yaml` for queue registration.

## Plan

1. Record preflight facts and create check-only queue scaffold.
2. Review runner code, CLI dispatch, focused tests, reports, and task evidence.
3. Run dynamic validation, negative CLI checks, hash checks, overclaiming scan,
   and secret scan.
4. Write check reports and task-local evidence.
5. Classify the result and recommend exactly one next task.

## Progress

- [x] Preflight started from a clean worktree.
- [x] Current HEAD verified as `04b6b6c98058e31a5beae1548bb0e2d7a5381f24`.
- [x] Check-only queue scaffold created.
- [x] Static implementation review complete.
- [x] Dynamic validation complete.
- [x] Check report written.
- [x] Task stopped at `needs_review`.

## Findings

- Result: `PASS_WITH_WARNINGS`.
- No boundary violation, canonical fixture mutation, overclaiming, secret marker,
  rollback execution, target repo mutation, active repo apply, branch/worktree
  mutation, merge, push, release, GitHub mutation, Gateway call, network call,
  or provider/model call was observed.
- Non-blocking warning: unsupported operation rejection exists in
  `ScopedExecutor.apply`, but the current focused tests do not directly exercise
  that helper path. This belongs in `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01`.

## Validation Intent

- Git preflight and commit identity checks.
- Task status, inspect, and evidence checks for the checked task.
- Lifecycle fixture status/run/verify checks.
- Lifecycle schema, scoped transaction, managed-section, and transaction status checks.
- Focused lifecycle runner tests and existing apply tests.
- Negative CLI checks for unsupported scenario and modes.
- JSON parse and report-path checks.
- Boundary hash checks around fresh runner invocation.
- Overclaiming and secret marker scans.
- `git diff --check`, commit check if committing.

## Recovery

If interrupted, inspect `status.yaml`, `.aide/reports/lifecycle-fixture-runner-check/check-report.json`,
and `git status --short` before continuing. Generated report churn outside the
check allowlist should be restored unless explicitly recorded as evidence.
