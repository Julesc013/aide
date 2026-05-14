# Root Recycling Framework v0

Q40 adds AIDE's first deterministic Root Recycling Framework. It inventories
top-level roots, classifies root status and risk, assigns per-file fate
candidates, records exceptions, and writes no-apply root recycling plans.

Q40 does not move roots, move files, delete files, rewrite references, absorb
tools, apply move/salvage/path-alias maps, mutate target repositories, mutate
branches, call providers/models, or use network calls.

## Why It Exists

Prompts such as `clean up the repo`, `move old roots`, or `delete stale XStack`
are unsafe when acted on directly. Q40 makes the first safe step mechanical:

1. inventory roots;
2. classify root roles and risks;
3. assign per-file fate candidates;
4. record exceptions and retirement conditions;
5. produce a no-apply plan for review.

Any future mutation still requires reviewed Q41/Q42-or-later work with concrete
move maps, salvage maps, aliases, validation, rollback, and evidence.

## Policies And Schemas

Portable policy files:

- `.aide/policies/root-recycling.yaml`
- `.aide/policies/root-inventory.yaml`
- `.aide/policies/root-fates.yaml`
- `.aide/policies/root-exceptions.yaml`
- `.aide/policies/root-risk.yaml`

Portable schemas:

- `.aide/refactors/root-inventory.schema.json`
- `.aide/refactors/root-record.schema.json`
- `.aide/refactors/root-file-classification.schema.json`
- `.aide/refactors/root-recycling-plan.schema.json`
- `.aide/refactors/root-exception.schema.json`
- `.aide/refactors/root-retirement.schema.json`
- `.aide/refactors/root-risk.schema.json`

## Commands

```text
py -3 .aide/scripts/aide_lite.py roots inventory
py -3 .aide/scripts/aide_lite.py roots classify
py -3 .aide/scripts/aide_lite.py roots plan
py -3 .aide/scripts/aide_lite.py roots validate
py -3 .aide/scripts/aide_lite.py roots status
py -3 .aide/scripts/aide_lite.py roots explain-root .aide
py -3 .aide/scripts/aide_lite.py roots explain-file .aide/scripts/aide_lite.py
```

Generated AIDE-local outputs:

- `.aide/roots/latest-root-inventory.json`
- `.aide/roots/latest-root-inventory.md`
- `.aide/roots/latest-root-classification.json`
- `.aide/roots/latest-root-classification.md`
- `.aide/roots/latest-root-recycling-plan.json`
- `.aide/roots/latest-root-recycling-plan.md`
- `.aide/roots/root-exceptions.json`
- `.aide/roots/root-risk-summary.md`

These are source-repo evidence. Target repositories must generate their own
root outputs after import.

## File Fates

Q40 defines these candidate fates:

- `keep`
- `wrap`
- `adapt`
- `extract`
- `convert`
- `archive`
- `drop_candidate`
- `shim`
- `alias`
- `unknown`

`drop_candidate` is not deletion approval. `archive` is not an applied move.
`shim` and `alias` are planned only. Every mutating future fate requires review,
evidence, validation, rollback notes, and an apply-capable queue item.

## Root Risks

Root risks are deterministic hints. Q40 detects identity-sensitive,
build-sensitive, authority-sensitive, generated-sensitive, mixed, unknown, and
local-state roots using path, kind, status, owner, generated/evidence, and
extension heuristics. These risks help prioritize review. They do not prove
semantic ownership and do not authorize mutation.

## Dominium Use

Dominium can later use the same framework to inventory roots such as `core/`,
`control/`, `data/`, `packs/`, `profiles/`, `bundles/`, `compat/`, `lib/`,
`safety/`, `security/`, `specs/`, `updates/`, `meta/`, `governance/`,
`validation/`, `templates/`, and `net/`. Q40 does not hard-code those roots as
AIDE truth and does not mutate Dominium.

## Export Boundary

The export pack carries portable root policies, schemas, tests, golden tasks,
and this reference doc. It excludes source-generated `.aide/roots/latest-*`,
`root-exceptions.json`, and `root-risk-summary.md` outputs as target truth.

## Q41 Handoff

Q41 Existing Tool Absorption v0 is next because tool absorption needs root
inventory and fate candidates before deciding whether existing tools should be
kept, wrapped, adapted, extracted, aliased, or left for review.
