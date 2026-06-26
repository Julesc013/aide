# AIDE-BUILD-PROJECT-LOCK-V0-01 ExecPlan

## Objective

Build ProjectLock v0 as the target-owned exact selection of one accepted
DistributionManifest and selected components.

## Scope

Allowed implementation surfaces:

- `.aide/protocol/aide-project-lock-v0.schema.json`
- `core/protocol/project_lock.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_project_lock_v0.py`
- `.aide/fixtures/project-lock-v0/**`
- `.aide/reports/project-lock-v0/**`

Allowed governance/evidence surfaces:

- `.aide/queue/AIDE-BUILD-PROJECT-LOCK-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Plan

1. Confirm DistributionManifest v1 has been accepted with zero material findings.
2. Add a Draft 2020-12 ProjectLock schema with explicit extension maps.
3. Add a deterministic helper that builds and validates a lock against an accepted DistributionManifest.
4. Add AIDE Lite `project-lock status/project/validate` commands.
5. Add valid and invalid fixtures plus focused tests.
6. Generate reports and task-local evidence.
7. Run focused and regression validation.
8. Stop at `needs_review` and recommend `AIDE-CHECK-PROJECT-LOCK-V0-01`.

## Boundaries

ProjectLock v0 is metadata and selection only. It is not install truth, an
install plan, admission, authorization, or target mutation authority.

## Result

`PASS_WITH_WARNINGS`; ready for independent check.
