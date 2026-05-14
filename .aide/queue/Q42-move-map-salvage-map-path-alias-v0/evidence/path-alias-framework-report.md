# Path Alias Framework Report

## Policy And Schemas

- Policy: `.aide/policies/path-aliases.yaml`
- Alias schema: `.aide/refactors/path-aliases.schema.json`
- Entry schema: `.aide/refactors/path-alias-entry.schema.json`
- Portable template: `.aide/refactors/path-aliases.template.yaml`

Q42 defines compatibility aliases, temporary shims, documentation redirects,
import aliases, generated projection aliases, and historical aliases as future
planning concepts only.

## Current Output

- YAML: `.aide/refactors/path-aliases.yaml`
- Markdown: `.aide/refactors/path-aliases.md`
- Alias entries: 0
- `no_apply`: true
- `active_aliases_created`: false
- `shims_created`: false

No AIDE-local alias is proposed because the current move map contains no
candidate moves. The exported pack includes schemas and the portable template,
not the source-generated current alias plan.

## Boundary

No alias or shim was created. Future aliases require a reviewed apply-capable
phase with validation and retirement conditions.
