# Q41 Tool Absorption Framework Report

Q41 adds a deterministic, repo-local, no-execution framework for discovering
and planning around existing management tools.

## Policy And Schema Surface

- Policies: `.aide/policies/tool-absorption.yaml`, `tool-inventory.yaml`, `tool-fates.yaml`, `tool-wrapping.yaml`, `tool-risk.yaml`, and `tool-capabilities.yaml`.
- Schemas: `.aide/tools/tool-inventory.schema.json`, `tool-record.schema.json`, `tool-capability.schema.json`, `tool-wrap-plan.schema.json`, `tool-adapter-map.schema.json`, `tool-risk.schema.json`, `tool-retirement.schema.json`, and `tool-evidence.schema.json`.
- Generated advisory outputs: `.aide/tools/latest-tool-inventory.*`, `latest-tool-classification.*`, `latest-tool-wrap-plan.*`, `latest-tool-adapter-map.*`, and `tool-risk-summary.md`.

## Command Surface

- `tools inventory`
- `tools classify`
- `tools wrap-plan`
- `tools validate`
- `tools status`
- `tools explain-tool PATH_OR_ID`
- `tools capabilities`

## Safety Guarantees

- Unknown discovered tools are never executed.
- Wrapper plans are documentation and future WorkUnit inputs only.
- `execution_allowed` is false by default.
- `apply_allowed` is false by default.
- `drop_candidate` is not deletion approval.
- Q41 does not delete, rename, migrate, wrap-execute, or mutate target repos.

## Integration Note

Q41 consumes Q37 repo intelligence, Q38 quality, Q39 refactor, and Q40 root
outputs by reference. It does not inline full inventories or treat source AIDE
tool outputs as target truth.
