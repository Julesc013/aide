# Q40 Root Recycling Framework v0 ExecPlan

## Objective

Implement a deterministic, repo-local root recycling framework that inventories
top-level roots, classifies root roles and file fates, records root risk and
exceptions, and produces no-apply planning artifacts for future root cleanup.

## Scope

Allowed work is limited to the Q40 queue packet, root recycling policies,
root schemas under `.aide/refactors/`, generated root reports under
`.aide/roots/`, AIDE Lite roots commands, tests, golden tasks, documentation,
the export pack, and Q41 task-packet regeneration.

## Non-Goals

- No file moves or deletes.
- No root moves or deletes.
- No reference rewrites.
- No tool absorption or migration.
- No target repo mutation.
- No provider/model/network calls.
- No current move-map, salvage-map, path-alias, install, upgrade, repair,
  rollback, or release implementation.

## Dependencies

- Q36 intent compiler and WorkUnit sizing posture.
- Q37 repo intelligence outputs.
- Q38 file quality ledger outputs.
- Q39 no-apply refactor control schemas and policy.

## Plan

1. Create the Q40 queue packet and review-gated status.
2. Define root recycling policies and root schemas.
3. Add AIDE Lite `roots` commands for inventory, classification, no-apply plan,
   validation, status, and explanation.
4. Add deterministic tests and golden tasks for root policy, schema, fate, and
   no-apply behavior.
5. Generate AIDE-local root artifacts and evidence.
6. Update documentation and export portable root recycling support.
7. Run validation and stop at `needs_review`.

## Progress

- [x] Q40 queue packet created.
- [ ] Root policies and schemas created.
- [ ] AIDE Lite roots commands implemented.
- [ ] Tests and golden tasks added.
- [ ] Root artifacts generated.
- [ ] Documentation and export pack updated.
- [ ] Validation evidence written.

## Recovery Notes

Q40 artifacts are dry-run evidence. If interrupted, resume by running
`py -3 .aide/scripts/aide_lite.py roots status`, then regenerate with
`roots inventory`, `roots classify`, `roots plan`, and `roots validate`.
Do not apply root moves or deletes during recovery.
