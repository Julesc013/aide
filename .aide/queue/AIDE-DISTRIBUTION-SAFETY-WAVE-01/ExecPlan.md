# ExecPlan: AIDE-DISTRIBUTION-SAFETY-WAVE-01

## Objective

Create the serialized Distribution Safety Wave plan that governs AIDE Lite install, update, rollback, uninstall, fixture, canary, and public-readiness work without granting downstream apply or publish authority.

## Scope

Allowed paths are limited to this queue task directory, `.aide/reports/distribution-safety-wave-01/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

This task is planning and queue materialization only. It does not implement InstallRecord, MigrationRecord, UpdatePlan, RollbackBundle, UpdateReceipt, DistributionApplyEngine, self-consumer fixtures, canary profiles, release archives, or public readiness acceptance.

## Dependencies

- `AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`
- `AIDE-ACCEPT-PROJECT-LOCK-V0-01`
- `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`

## Work Plan

1. Verify live repo truth and accepted ownership boundary.
2. Materialize the wave task packet and status.
3. Write the dependency map, responsibility map, no-apply/no-publish boundary, validation matrix, repair-routing matrix, stop-condition matrix, canary rationale, and next-task prompt.
4. Update `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
5. Run parse, task inspect/evidence, broad validation, safety scans, and diff checks.
6. Commit the wave-controller task and run `commit check --latest`.

## Validation Intent

Validation is structural and report-oriented: JSON/YAML parse, task inspect/evidence, broad AIDE validation, path and secret-like scans, source-output misuse scan, Git diff checks, and commit-policy check after commit.

## Stop Conditions

Stop at `needs_review`. Do not start `AIDE-BUILD-INSTALL-RECORD-V0-01` in this task, even though its prompt is produced as the next concrete task.
