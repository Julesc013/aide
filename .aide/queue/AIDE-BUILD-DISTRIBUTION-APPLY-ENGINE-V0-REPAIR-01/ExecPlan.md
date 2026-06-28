# ExecPlan: AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01

## Objective

Repair `distribution_apply_engine_v0` so fixture execution is gated on an accepted distribution apply context before any operation can run.

## Scope

- Add an internal accepted-context loader and validator.
- Bind executable scenarios to accepted DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle, and UpdateReceipt acceptance records.
- Refuse missing or mismatched UpdatePlan and RollbackBundle refs.
- Refuse predecessor mismatches with explicit reason codes.
- Refuse missing or non-accepted context before temp workspace execution.
- Add adversarial fixtures and tests for the four material findings.
- Regenerate fixture and report outputs.
- Stop at `needs_review` and recommend the independent repair-check.

## Non-Goals

- No DistributionApplyEngine acceptance.
- No repair-check execution as this task's queue state.
- No self-consumer fixture or canary.
- No real target apply, source repo self-apply, release publication, external repo mutation, provider/model/network calls, or branch/worktree automation.

## Progress

- [x] Confirmed live queue route from `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`.
- [x] Added `core/distribution/apply_context.py`.
- [x] Required accepted context validation before static refusal, temp workspace setup, operation execution, rollback verification, or receipt output.
- [x] Added nine adversarial context-binding scenarios.
- [x] Added focused regression tests for context refusals and missing acceptance reports.
- [x] Regenerated DistributionApplyEngine fixtures and reports.
- [x] Ran focused validation and adversarial scenario commands.
- [x] Wrote repair evidence, reports, and queue routing.

## Outcome

Result: `PASS_WITH_WARNINGS`.

The four material findings from `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01` are repaired in the proposed implementation. DistributionApplyEngine v0 is still not accepted and must pass `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01`.

## Validation Plan

Run compile checks, focused tests, `distribution-apply status/plan/run/verify`, explicit adversarial scenario runs for the repaired findings, predecessor regression validations, Q43-Q48 no-apply/no-publish validators, broad AIDE validation, task inspect/evidence, path and credential scans, diff checks, and commit-policy validation.

## Recovery

If the independent repair-check finds material issues, route to a bounded second repair cycle. Do not accept DistributionApplyEngine v0 directly from this repair task.
