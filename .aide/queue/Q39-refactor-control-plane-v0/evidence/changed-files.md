# Q39 Changed Files

## Queue Packet

- `.aide/queue/index.yaml`
- `.aide/queue/Q39-refactor-control-plane-v0/task.yaml`
- `.aide/queue/Q39-refactor-control-plane-v0/ExecPlan.md`
- `.aide/queue/Q39-refactor-control-plane-v0/prompt.md`
- `.aide/queue/Q39-refactor-control-plane-v0/status.yaml`
- `.aide/queue/Q39-refactor-control-plane-v0/evidence/*.md`

## Policies And Schemas

- `.aide/policies/refactor.yaml`
- `.aide/policies/migration.yaml`
- `.aide/policies/refactor-safety.yaml`
- `.aide/policies/refactor-evidence.yaml`
- `.aide/policies/refactor-application.yaml`
- `.aide/refactors/README.md`
- `.aide/refactors/refactor-plan.schema.json`
- `.aide/refactors/refactor-operation.schema.json`
- `.aide/refactors/move-map.schema.json`
- `.aide/refactors/salvage-map.schema.json`
- `.aide/refactors/path-aliases.schema.json`
- `.aide/refactors/migration-ledger.schema.json`
- `.aide/refactors/rollback-notes.schema.json`
- `.aide/refactors/refactor-risk.schema.json`
- `.aide/refactors/refactor-validation.schema.json`

## Commands And Generated Readiness

- `.aide/scripts/aide_lite.py`
- `.aide/refactors/latest-refactor-readiness.json`
- `.aide/refactors/latest-refactor-readiness.md`
- `.aide/refactors/latest-refactor-plan.example.json`
- `.aide/refactors/latest-refactor-plan.example.md`
- `.aide/refactors/migration-ledger.example.jsonl`
- `.aide/context/latest-task-packet.md`

## Tests And Golden Tasks

- `.aide/scripts/tests/test_q39_refactor_control.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/evals/golden-tasks/refactor_policy_golden/**`
- `.aide/evals/golden-tasks/migration_policy_golden/**`
- `.aide/evals/golden-tasks/refactor_plan_schema_golden/**`
- `.aide/evals/golden-tasks/move_map_schema_golden/**`
- `.aide/evals/golden-tasks/salvage_map_schema_golden/**`
- `.aide/evals/golden-tasks/path_alias_schema_golden/**`
- `.aide/evals/golden-tasks/migration_ledger_schema_golden/**`
- `.aide/evals/golden-tasks/refactor_no_apply_golden/**`

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `.aide/commands/catalog.yaml`
- `docs/reference/README.md`
- `docs/reference/refactor-control-plane.md`
- `docs/reference/file-quality-ledger.md`
- `docs/reference/repo-intelligence-index.md`
- `docs/reference/cross-repo-pack-export-import.md`

## Export Pack

- `.aide/export/aide-lite-pack-v0/**`

The export pack includes portable Q39 policies, schemas, README, AIDE Lite
command support, tests, golden tasks, and docs. It does not export
source-generated latest refactor readiness or example plan artifacts as target
truth.
