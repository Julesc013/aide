# Changed Files

## Queue And Evidence

- `.aide/queue/Q43-install-plan-model-v0/**`: Q43 task packet, ExecPlan, status, prompt summary, and evidence.
- `.aide/queue/index.yaml`: Q43 recorded as implemented for `needs_review`.

## Install Policies

- `.aide/policies/install.yaml`
- `.aide/policies/install-preservation.yaml`
- `.aide/policies/install-ownership.yaml`
- `.aide/policies/install-conflicts.yaml`
- `.aide/policies/install-migrations.yaml`
- `.aide/policies/install-verification.yaml`

## Install Schemas And Outputs

- `.aide/install/README.md`
- `.aide/install/*.schema.json`
- `.aide/install/latest-install-observation.json`
- `.aide/install/latest-install-observation.md`
- `.aide/install/latest-install-plan.json`
- `.aide/install/latest-install-plan.md`
- `.aide/install/latest-install-dry-run.json`
- `.aide/install/latest-install-dry-run.md`
- `.aide/install/latest-ownership-ledger.example.json`
- `.aide/install/latest-conflict-report.json`
- `.aide/install/latest-conflict-report.md`
- `.aide/install/latest-preservation-report.md`
- `.aide/install/latest-verification-plan.md`

## Command Surface, Tests, And Golden Tasks

- `.aide/scripts/aide_lite.py`: added `install observe/plan/dry-run/validate/status/explain/ownership/conflicts`.
- `.aide/scripts/tests/test_q43_install_plan.py`: Q43 no-apply install planning tests.
- `.aide/evals/golden-tasks/catalog.yaml`: Q43 golden tasks registered.
- `.aide/evals/golden-tasks/install_*`: Q43 deterministic install golden tasks.

## Documentation And Catalogs

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `.aide/commands/catalog.yaml`
- `docs/reference/aide-install-model.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `docs/reference/move-salvage-path-aliases.md`

## Export And Context

- `.aide/export/aide-lite-pack-v0/**`: refreshed portable pack with Q43 install support and without source-generated install plans as target truth.
- `.aide/context/latest-task-packet.md`: regenerated for Q44 Repair / Doctor Model v0.
