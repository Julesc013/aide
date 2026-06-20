# Findings

## MCP-CHECK-001

Severity: material

List pagination fixtures emit `null` for optional cursor fields:

- `prompts-list-request.json`: `params.cursor`
- `prompts-list-result.json`: `result.nextCursor`
- `resources-list-request.json`: `params.cursor`
- `resources-list-result.json`: `result.nextCursor`
- `tools-list-request.json`: `params.cursor`
- `tools-list-result.json`: `result.nextCursor`

Expected: omit absent cursor fields or emit strings only.

## MCP-CHECK-002

Severity: material

`resource-not-found-refusal.json` uses `error.code: -32043`.

Expected: `-32002` for the pinned MCP resource-not-found mapping.

## Disposition

Recommend `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`.
