# JSON-RPC Review

All MCP fixture files parse as JSON and carry `jsonrpc: "2.0"`.

Independent invariant review found one material fixture-shape class:

- `prompts-list-request.json`: `params.cursor` is `null`
- `prompts-list-result.json`: `result.nextCursor` is `null`
- `resources-list-request.json`: `params.cursor` is `null`
- `resources-list-result.json`: `result.nextCursor` is `null`
- `tools-list-request.json`: `params.cursor` is `null`
- `tools-list-result.json`: `result.nextCursor` is `null`

Under the pinned subset checked by this task, absent cursors must be omitted or
represented by strings. `null` is a material validation failure.
