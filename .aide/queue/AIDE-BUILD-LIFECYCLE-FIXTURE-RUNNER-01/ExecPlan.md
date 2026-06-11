# ExecPlan

## Objective

Implement one protocol-shaped vertical slice for lifecycle fixture execution:

canonical fixture -> temp workspace -> scoped managed-section apply -> verification -> evidence.

## Scope

This WorkUnit authorizes implementation only for `lifecycle-fixture` temp-runner behavior. The runner may use the existing `install-managed-section` generated plan and static fixture data as read-only inputs, copy the selected fixture target to a temporary workspace, apply one scoped managed-section mutation inside that temporary workspace, verify the postimage and evidence, and write reports under `.aide/reports/lifecycle-fixture-runner/**`.

## Non-Goals

- No broad AIDE kernel scaffold.
- No service, Commander, mobile, host, provider, plugin, branch/worktree, or adapter framework.
- No lifecycle apply against the active repository.
- No canonical fixture target mutation.
- No generated lifecycle plan or expected report mutation.
- No rollback or uninstall execution.
- No target repository mutation.
- No branch/worktree, merge, push, promotion, release, GitHub, provider/model, Gateway, or network action.

## Allowed Paths

The allowlist is recorded in `task.yaml`. Code changes are limited to:

- `core/apply/lifecycle_fixture_runner.py`
- `core/apply/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lifecycle_fixture_runner.py`

Queue, report, intake, planning, and evidence paths are limited to the paths in `task.yaml`.

## Plan

1. Materialize this queue WorkUnit with explicit implementation authority.
2. Add a small lifecycle fixture runner module with `ScenarioLoader`, `TransactionCompiler`, `ScopedExecutor`, `FixtureVerifier`, and `EvidenceReporter`.
3. Add thin CLI dispatch for `lifecycle-fixture status`, `run`, and `verify`.
4. Add focused tests for parser registration, temp-only mutation, fail-closed verification, path-jail rejection, and capability labels.
5. Run targeted tests and command smoke checks.
6. Write evidence and move the task to `needs_review`.

## Progress

- [x] Queue packet created with `authorizes_implementation: true`.
- [x] Runner module implemented.
- [x] CLI dispatch added.
- [x] Tests added.
- [x] Validation run.
- [x] Evidence written.
- [x] Status moved to `needs_review`.
- [x] Attached prompt gap-fix added stricter report aliases, future/unfinished-work reports, expanded focused tests, and explicit forbidden-operation evidence.

## Discoveries

- The static expected postimage for `install-managed-section` changes the
  managed-section BEGIN marker metadata as well as the generated section body.
  The runner therefore performs a full marker-bounded block replacement inside
  the temp workspace while reusing the existing managed-section parser and hash
  logic. This keeps manual content outside the markers preserved and avoids
  changing the existing content-only scoped transaction executor.

## Current Facts To Verify

- The selected scenario is `install-managed-section`.
- The source plan is `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`.
- The canonical target fixture is `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/**`.
- The expected state is `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/**`.
- The static rollback-compatible record is `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`.
- The existing scoped transaction executor already implements path normalization, protected-path checks, symlink escape checks, single-operation apply, postimage verification, and rollback-compatible record output.

## Idempotence And Recovery

Rerunning `lifecycle-fixture run --scenario install-managed-section --mode apply-temp` should create a new temp workspace and overwrite the latest run pointer without mutating canonical fixtures. `lifecycle-fixture verify` should validate the latest completed run by default and fail closed if required evidence is missing or contradictory.

If implementation is interrupted, resume from this plan and inspect `status.yaml`, `.aide/reports/lifecycle-fixture-runner/latest-run.json`, and the git diff before continuing.

## Validation Intent

- Parser registration test for lifecycle-fixture commands.
- Targeted lifecycle fixture runner tests.
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py test`
- JSON parse checks for lifecycle fixture runner reports
- YAML-like structural checks for changed task/status/index files
- `git diff --check`

## Evidence

Evidence will be written under `evidence/` and must include changed files, validation commands/results, path boundary confirmation, capability labels, generated report refs, blockers/deferrals, and proof that canonical fixture files were not changed.

## Retrospective

The implemented slice adds only the runner module, CLI dispatch, focused tests,
queue records, and generated lifecycle fixture runner reports. It does not
create kernel directories, provider adapters, service behavior, Commander
behavior, branch/worktree automation, rollback execution, target-repo mutation,
or network/provider/Gateway behavior. A follow-up alignment pass added report
aliases `verify.json` and `verify.md`, runner-level future and unfinished work
reports, and task-local future/unfinished/no-forbidden-ops evidence requested
by the attached full build prompt.
