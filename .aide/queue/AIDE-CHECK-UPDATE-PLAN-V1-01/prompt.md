# Prompt: AIDE-CHECK-UPDATE-PLAN-V1-01

Create and process `AIDE-CHECK-UPDATE-PLAN-V1-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

This is a check-only task. Do not repair implementation, accept UpdatePlan v1, begin RollbackBundle, begin UpdateReceipt, start DistributionApplyEngine, mutate target repositories, publish releases, create tags/uploads/GitHub Releases, call provider/model/network services, or perform install/update/migration/repair/rollback/uninstall apply.

Verify:

- `AIDE-BUILD-UPDATE-PLAN-V1-01` exists, is complete, and stopped at `needs_review`.
- Build task `missing_evidence` is `0`.
- UpdatePlan schema, helper, fixtures, CLI commands, tests, reports, and queue packet exist.
- UpdatePlan is dry-run/no-apply and does not claim update/apply authority.
- Accepted predecessor compatibility remains intact for DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord.
- Planned operation classes are represented in schema/helper and semantically validated.
- Required positive and negative fixture cases exist and pass.
- Unknown optional extensions are preserved/tolerated.
- Unknown required features fail closed.
- The projected unknown and never-touch conflicts are warning-class because they fail closed and do not claim apply authority.
- Reports and evidence do not leak local absolute paths, secrets, source-state-as-target-truth, or source latest output as target truth.

If the check passes with zero material findings and zero missing evidence, recommend exactly `AIDE-ACCEPT-UPDATE-PLAN-V1-01`.
