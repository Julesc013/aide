# Changed Files

## Queue packet and evidence

- `.aide/queue/Q45-upgrade-model-v0/**`: Q45 task packet, ExecPlan, status, prompt copy, and evidence.
- `.aide/queue/index.yaml`: adds Q45 and marks it ready for review.

## Upgrade policies and schemas

- `.aide/policies/upgrade.yaml`
- `.aide/policies/upgrade-compatibility.yaml`
- `.aide/policies/upgrade-preservation.yaml`
- `.aide/policies/upgrade-conflicts.yaml`
- `.aide/policies/upgrade-migrations.yaml`
- `.aide/policies/upgrade-verification.yaml`
- `.aide/upgrade/README.md`
- `.aide/upgrade/*.schema.json`

## AIDE Lite command surface

- `.aide/scripts/aide_lite.py`: adds `upgrade observe-current`, `observe-source`, `compare`, `plan`, `dry-run`, `validate`, `status`, `explain`, `compatibility`, `conflicts`, and `migrations`.
- `.aide/commands/catalog.yaml`: documents the Q45 upgrade commands.

## Tests and golden tasks

- `.aide/scripts/tests/test_q45_upgrade_model.py`
- `.aide/evals/golden-tasks/catalog.yaml`

## Generated Q45 artifacts

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

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `docs/reference/aide-upgrade-model.md`
- `docs/reference/aide-install-model.md`
- `docs/reference/aide-repair-model.md`
- `docs/reference/cross-repo-pack-export-import.md`

## Export pack and next packet

- `.aide/export/aide-lite-pack-v0/**`: regenerated portable pack support for upgrade planning.
- `.aide/context/latest-task-packet.md`: regenerated for Q46 Rollback / Uninstall Model v0.
