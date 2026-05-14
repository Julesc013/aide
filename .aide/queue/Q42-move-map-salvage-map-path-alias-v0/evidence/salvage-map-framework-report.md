# Salvage Map Framework Report

## Policy And Schemas

- Policy: `.aide/policies/salvage-map.yaml`
- Map schema: `.aide/refactors/salvage-map.schema.json`
- Entry schema: `.aide/refactors/salvage-map-entry.schema.json`

The policy defines fates `keep`, `wrap`, `adapt`, `extract`, `convert`,
`archive`, `drop_candidate`, `shim`, `alias`, and `unknown`. It explicitly
states that `drop_candidate` is not deletion approval and that Q42 performs no
salvage extraction.

## Current Output

- JSON: `.aide/refactors/current-salvage-map.json`
- Markdown: `.aide/refactors/current-salvage-map.md`
- Status: `candidate`
- Entries: 20
- `no_apply`: true

The current candidates are derived conservatively from Q41 tool wrap-plan
outputs. Each entry has `apply_allowed: false`; most are `wrap` candidates for
existing AIDE evidence, template, context, changelog, or export artifacts.

## Caveats

- Salvage entries are review candidates only.
- `wrap` is not active execution.
- `extract` or `convert` fates would still require a future reviewed WorkUnit.
- No file contents were extracted or rewritten.
