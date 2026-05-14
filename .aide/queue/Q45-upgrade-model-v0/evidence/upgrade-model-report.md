# Upgrade Model Report

Q45 adds the first generic AIDE upgrade planning model. It observes the current install, observes the source export pack, compares differences, creates a preservation-first plan, produces a dry-run, and validates that no operation can apply in Q45.

## Policies

- `.aide/policies/upgrade.yaml`
- `.aide/policies/upgrade-compatibility.yaml`
- `.aide/policies/upgrade-preservation.yaml`
- `.aide/policies/upgrade-conflicts.yaml`
- `.aide/policies/upgrade-migrations.yaml`
- `.aide/policies/upgrade-verification.yaml`

## Schemas

- `.aide/upgrade/current-install-observation.schema.json`
- `.aide/upgrade/source-pack-observation.schema.json`
- `.aide/upgrade/upgrade-comparison.schema.json`
- `.aide/upgrade/upgrade-plan.schema.json`
- `.aide/upgrade/upgrade-operation.schema.json`
- `.aide/upgrade/upgrade-dry-run.schema.json`
- `.aide/upgrade/upgrade-conflict-report.schema.json`
- `.aide/upgrade/upgrade-migration-report.schema.json`
- `.aide/upgrade/upgrade-verification.schema.json`
- `.aide/upgrade/upgrade-compatibility-report.schema.json`

## Commands

- `upgrade observe-current`
- `upgrade observe-source`
- `upgrade compare`
- `upgrade plan`
- `upgrade dry-run`
- `upgrade validate`
- `upgrade status`
- `upgrade explain PATH_OR_ISSUE`
- `upgrade compatibility`
- `upgrade conflicts`
- `upgrade migrations`

## Generated Artifacts

- `.aide/upgrade/latest-current-install-observation.json`
- `.aide/upgrade/latest-current-install-observation.md`
- `.aide/upgrade/latest-source-pack-observation.json`
- `.aide/upgrade/latest-source-pack-observation.md`
- `.aide/upgrade/latest-upgrade-comparison.json`
- `.aide/upgrade/latest-upgrade-comparison.md`
- `.aide/upgrade/latest-upgrade-plan.json`
- `.aide/upgrade/latest-upgrade-plan.md`
- `.aide/upgrade/latest-upgrade-dry-run.json`
- `.aide/upgrade/latest-upgrade-dry-run.md`
- `.aide/upgrade/latest-upgrade-conflict-report.json`
- `.aide/upgrade/latest-upgrade-conflict-report.md`
- `.aide/upgrade/latest-upgrade-migration-report.md`
- `.aide/upgrade/latest-upgrade-compatibility-report.md`
- `.aide/upgrade/latest-upgrade-verification-plan.md`

## No-Apply Guarantee

- `no_apply` is true in generated Q45 upgrade JSON outputs.
- Every generated upgrade operation has `apply_allowed: false`.
- Every generated upgrade operation has `overwrite_allowed: false` and `delete_allowed: false`.
- Q45 commands write only advisory upgrade artifacts under `.aide/upgrade/**`.
- Q45 does not install, repair, upgrade, roll back, uninstall, overwrite, delete, move, rewrite, or migrate files.
