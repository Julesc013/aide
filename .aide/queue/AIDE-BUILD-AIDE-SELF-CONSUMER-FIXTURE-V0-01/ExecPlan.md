# ExecPlan: AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01

## Objective

Build `aide_self_consumer_fixture_v0` as the first AIDE-like target fixture after accepted DistributionApplyEngine v0.

## Scope

Allowed writes:

- `.aide/fixtures/aide-self-consumer-fixture-v0/**`
- `.aide/reports/aide-self-consumer-fixture-v0/**`
- `.aide/scripts/tests/test_aide_self_consumer_fixture_v0.py`
- `.aide/queue/AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Non-Goals

No real target apply, source repo apply, install/update/migration/rollback/repair/uninstall apply against a real target, project canaries, release generation, public readiness, tag, upload, GitHub Release, provider/model/network call, external repo mutation, branch/worktree automation, check task, or acceptance task is authorized.

## Progress

- [x] Verified live repo route after `AIDE-ACCEPT-DISTRIBUTION-APPLY-ENGINE-V0-01`.
- [x] Materialized self-consumer fixture manifest, lifecycle scenarios, states, and ownership/lifecycle manifests.
- [x] Wrote focused tests for the fixture boundary and report consistency.
- [x] Wrote reports and task-local evidence.
- [x] Run final validation and commit-policy check.

## Validation

Run the focused fixture test, distribution-apply verification, Q43-Q48 no-apply/no-publish validators, broad AIDE validation, task inspect/evidence, safety scans, diff checks, and commit-policy validation.

## Recovery

If resumed, inspect `status.yaml`, rerun the focused fixture test, verify the acceptance predecessor remains intact, and do not perform real target apply or source repo apply. Complete only missing fixture/report/evidence surfaces inside the allowed paths.
