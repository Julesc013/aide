# ExecPlan: AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01

## Objective

Build `distribution_apply_engine_v0` as a fixture-only, temp-workspace-only executor after accepted UpdateReceipt v0.

## Scope

- Add `core/distribution/**` helpers for temp workspace isolation, operation execution, rollback verification, and report rendering.
- Add `distribution-apply status/plan/run/verify` AIDE Lite commands.
- Add a deterministic scenario corpus under `.aide/fixtures/distribution-apply-engine-v0/**`.
- Add focused tests and reports proving managed file operations, managed section operations, preservation behavior, refusals, receipt output, rollback verification, canonical fixture preservation, and no target/source/release mutation.
- Add task-local evidence and queue routing to the independent check gate.

## Non-Goals

- No real target repository apply.
- No source repository self-apply.
- No release archive, tag, upload, or GitHub Release.
- No provider/model/network calls.
- No ScreenSave, Eureka, Dominium, or external repository mutation.
- No self-consumer fixture or canary materialization.
- No independent check or acceptance in this build task.

## Allowed Paths

- `core/distribution/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_distribution_apply_engine_v0.py`
- `.aide/fixtures/distribution-apply-engine-v0/**`
- `.aide/reports/distribution-apply-engine-v0/**`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Progress

- [x] Confirmed live repo state is clean and routed to `AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01`.
- [x] Added fixture-only distribution executor modules.
- [x] Added AIDE Lite `distribution-apply` CLI wiring.
- [x] Added focused tests for temp execution, refusals, rollback, fixture preservation, and CLI boundaries.
- [x] Generate fixtures and reports.
- [x] Run full validation and evidence scans.
- [x] Update status to `needs_review` and stop.

## Outcome

Result: `PASS_WITH_WARNINGS`.

DistributionApplyEngine v0 is proposed as fixture-only and temp-workspace-only. It executes accepted distribution update plan scenarios against copied fixture workspaces, emits UpdateReceipt-shaped fixture outputs, verifies rollback using RollbackBundle fixture data, verifies postimage digests, refuses unsafe operations, and verifies canonical fixture files remain unchanged.

Warnings:

- DistributionApplyEngine v0 remains proposed until independent check and acceptance.
- Execution is limited to committed fixture scenarios copied into temporary workspaces.
- This build does not authorize real target apply, source repo self-update, release publication, external repo mutation, self-consumer fixture, canaries, provider/model/network calls, or branch/worktree automation.

## Validation Plan

Run syntax checks, focused tests, `distribution-apply status/plan/run/verify`, predecessor protocol validations, Q43-Q48 no-apply/no-publish validators, broad AIDE validation, task inspect/evidence, canonical fixture preservation check, temp workspace isolation check, path, credential-pattern, and source-output scans, diff checks, and post-commit commit-policy validation.

## Recovery

The build is deterministic. Re-run `py -3 .aide/scripts/aide_lite.py distribution-apply verify` to regenerate the scenario corpus and reports. If validation fails, leave status as blocked or failed validation and do not proceed to check or acceptance.
