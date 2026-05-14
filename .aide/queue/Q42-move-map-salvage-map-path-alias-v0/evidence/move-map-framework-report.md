# Move Map Framework Report

## Policy And Schemas

- Policy: `.aide/policies/move-map.yaml`
- Map schema: `.aide/refactors/move-map.schema.json`
- Entry schema: `.aide/refactors/move-map-entry.schema.json`

The policy declares deterministic local candidate-only operation, dry-run-first
planning, `no_apply_in_q42`, no file moves, no file deletes, and no reference
rewrites.

## Command Surface

- `py -3 .aide/scripts/aide_lite.py refactor map`
- `py -3 .aide/scripts/aide_lite.py refactor move-map`
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`
- `py -3 .aide/scripts/aide_lite.py refactor map-status`

## Current Output

- JSON: `.aide/refactors/current-move-map.json`
- Markdown: `.aide/refactors/current-move-map.md`
- Status: `candidate`
- Entries: 0
- `no_apply`: true
- `file_moves`: false

Q42 intentionally emits a sparse move map for AIDE because no concrete root or
migration target has been selected by a reviewed task. Future target repos must
generate their own local maps.

## No-Apply Guarantee

`validate-map` passed and rejected mutation markers including
`"apply_allowed": true`, `safe_to_delete`, `deletion approved`,
`"file_moves": true`, `"file_deletes": true`, and
`"target_repo_mutation": true`.
