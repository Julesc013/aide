# Changed Files

## Queue Packet And Evidence

- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/task.yaml`
- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/ExecPlan.md`
- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/prompt.md`
- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/status.yaml`
- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/evidence/*.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q41-existing-tool-absorption-v0/status.yaml` metadata-only repair from `running` to `needs_review`.

## Policies

- `.aide/policies/move-map.yaml`
- `.aide/policies/salvage-map.yaml`
- `.aide/policies/path-aliases.yaml`
- `.aide/policies/reference-rewrite.yaml`
- `.aide/policies/migration-ledger.yaml`

## Schemas And Templates

- `.aide/refactors/move-map.schema.json`
- `.aide/refactors/move-map-entry.schema.json`
- `.aide/refactors/salvage-map.schema.json`
- `.aide/refactors/salvage-map-entry.schema.json`
- `.aide/refactors/path-aliases.schema.json`
- `.aide/refactors/path-alias-entry.schema.json`
- `.aide/refactors/path-aliases.template.yaml`
- `.aide/refactors/reference-rewrite-plan.schema.json`
- `.aide/refactors/reference-rewrite-entry.schema.json`
- `.aide/refactors/migration-ledger.schema.json`
- `.aide/refactors/migration-ledger-entry.schema.json`
- `.aide/refactors/map-validation-report.schema.json`

## AIDE Lite Commands And Tests

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q42_move_map_aliases.py`
- `.aide/evals/golden-tasks/catalog.yaml`
- `.aide/evals/golden-tasks/move_map_policy_golden/**`
- `.aide/evals/golden-tasks/salvage_map_policy_golden/**`
- `.aide/evals/golden-tasks/path_alias_policy_golden/**`
- `.aide/evals/golden-tasks/reference_rewrite_plan_golden/**`
- `.aide/evals/golden-tasks/migration_ledger_policy_golden/**`
- `.aide/evals/golden-tasks/refactor_map_no_apply_golden/**`
- `.aide/evals/golden-tasks/drop_candidate_not_delete_approval_golden/**`

## Generated Q42 Evidence Outputs

- `.aide/refactors/current-move-map.json`
- `.aide/refactors/current-move-map.md`
- `.aide/refactors/current-salvage-map.json`
- `.aide/refactors/current-salvage-map.md`
- `.aide/refactors/path-aliases.yaml`
- `.aide/refactors/path-aliases.md`
- `.aide/refactors/reference-rewrite-plan.json`
- `.aide/refactors/reference-rewrite-plan.md`
- `.aide/refactors/migration-ledger.draft.jsonl`
- `.aide/refactors/map-validation-report.json`
- `.aide/refactors/map-validation-report.md`

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `.aide/commands/catalog.yaml`
- `docs/reference/move-salvage-path-aliases.md`
- `docs/reference/refactor-control-plane.md`
- `docs/reference/root-recycling-framework.md`
- `docs/reference/tool-absorption.md`
- `docs/reference/cross-repo-pack-export-import.md`

## Export Pack And Context

- `.aide/export/aide-lite-pack-v0/**`
- `.aide/context/latest-task-packet.md`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`

## Not Changed

- No files were moved.
- No files were deleted.
- No references were rewritten.
- No aliases or shims were created.
- No target repositories were mutated.
