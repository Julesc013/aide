# Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml`: moved Q46 to `needs_review`.
- `.aide/queue/Q46-rollback-uninstall-model-v0/**`: task packet, ExecPlan,
  status, prompt copy, and evidence.
- `.aide/context/latest-task-packet.md`: regenerated for Q47 AIDE Lite Release
  Bundle v0.

## Policies

- `.aide/policies/rollback.yaml`
- `.aide/policies/rollback-classes.yaml`
- `.aide/policies/rollback-safety.yaml`
- `.aide/policies/rollback-verification.yaml`
- `.aide/policies/uninstall.yaml`
- `.aide/policies/uninstall-classes.yaml`
- `.aide/policies/uninstall-safety.yaml`
- `.aide/policies/uninstall-verification.yaml`

## Schemas And Generated Plans

- `.aide/rollback/**`: rollback schemas, README, latest observation, plan,
  dry-run, and verification plan.
- `.aide/uninstall/**`: uninstall schemas, README, latest observation, plan,
  dry-run, and verification plan.

## AIDE Lite, Tests, And Golden Tasks

- `.aide/scripts/aide_lite.py`: rollback and uninstall command families,
  validation gates, status/explain/classes behavior, and golden task runners.
- `.aide/scripts/tests/test_q46_rollback_uninstall.py`: no-apply rollback and
  uninstall tests.
- `.aide/evals/golden-tasks/catalog.yaml` and Q46 golden task directories.

## Documentation And Export

- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/aide-rollback-uninstall.md`
- `docs/reference/aide-install-model.md`
- `docs/reference/aide-repair-model.md`
- `docs/reference/aide-upgrade-model.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `.aide/export/aide-lite-pack-v0/**`
