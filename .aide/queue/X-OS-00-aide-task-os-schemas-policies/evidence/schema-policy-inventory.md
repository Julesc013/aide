# Schema And Policy Inventory

## Policies

- `.aide/policies/task-lifecycle.yaml`
- `.aide/policies/blockers.yaml`
- `.aide/policies/repair-loop.yaml`
- `.aide/policies/waves.yaml`
- `.aide/policies/checkpoints.yaml`
- `.aide/policies/dev-main-promotion.yaml`
- `.aide/policies/capability-reality.yaml`

## Schemas

- `.aide/tasks/workunit.schema.json`
- `.aide/tasks/task-attempt.schema.json`
- `.aide/tasks/blocker.schema.json`
- `.aide/tasks/repair-task.schema.json`
- `.aide/tasks/wave.schema.json`
- `.aide/tasks/checkpoint.schema.json`
- `.aide/ledgers/task-ledger.schema.json`
- `.aide/ledgers/blocker-ledger.schema.json`
- `.aide/ledgers/capability-ledger.schema.json`
- `.aide/ledgers/branch-provenance.schema.json`
- `.aide/ledgers/checkpoint-ledger.schema.json`

## Examples And Docs

- `.aide/examples/task-os/*.example.json`
- `docs/reference/task-os-v0.md`
- `docs/reference/workunit-lifecycle.md`
- `docs/reference/blocker-and-repair-model.md`
- `docs/reference/checkpoint-and-promotion-model.md`

## Validation Coverage

The Task OS validator checks required files, JSON object roots, required-field declarations, lifecycle states, blocker classes, blocker severities, capability states, no-apply anchors, example markers, and the absence of an implemented `task-os` command group.
