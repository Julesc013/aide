# AIDE-BUILD-ROLLBACK-BUNDLE-V0-01 ExecPlan

## Objective

Build `rollback_bundle_v0` as a no-apply rollback-preparation contract after accepted `update_plan_v1`.

## Scope

- Add RollbackBundle v0 schema, helper/projection/validation logic, CLI commands, fixtures, focused tests, generated reports, queue packet, and task-local evidence.
- Bind RollbackBundle to accepted UpdatePlan v1 and predecessor DistributionManifest, ProjectLock, OwnershipLedger, and InstallRecord records.
- Preserve rollback preparation as metadata only. No rollback execution or target mutation is authorized.

## Allowed Paths

- `.aide/protocol/aide-rollback-bundle-v0.schema.json`
- `core/protocol/rollback_bundle.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_rollback_bundle_v0.py`
- `.aide/fixtures/rollback-bundle-v0/**`
- `.aide/reports/rollback-bundle-v0/**`
- `.aide/queue/AIDE-BUILD-ROLLBACK-BUNDLE-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Non-Capabilities

This task does not implement rollback apply, update apply, install apply, migration apply, uninstall apply, target repo mutation, target scan authority, release archive creation, release publication, tags, uploads, GitHub Releases, provider/model/network calls, DistributionApplyEngine, UpdateReceipt, canaries, runtime, branch/worktree automation, or promotion.

## Milestones

- [x] Verify live repo truth and predecessor UpdatePlan acceptance.
- [x] Add RollbackBundle schema and helper.
- [x] Add AIDE Lite CLI commands.
- [x] Add fixture corpus and focused tests.
- [x] Generate RollbackBundle reports.
- [x] Write queue packet and task evidence.
- [x] Complete final validation, stage, commit, and stop at review gate.

## Validation Intent

Run focused RollbackBundle tests, RollbackBundle status/project/validate commands, predecessor regressions, Q43-Q48 no-apply/no-publish validators, broad AIDE validation, task inspect/evidence, path/secret/source-output scans, diff checks, staged diff checks, and commit-policy check.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, proposed capability exactly `rollback_bundle_v0`, and next task exactly `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`.
