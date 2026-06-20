# JSON-RPC Review

All MCP fixture files parse and carry `jsonrpc: "2.0"`.

Material failure:

```text
prompts-list-request.json     params.cursor = null
prompts-list-result.json      result.nextCursor = null
resources-list-request.json   params.cursor = null
resources-list-result.json    result.nextCursor = null
tools-list-request.json       params.cursor = null
tools-list-result.json        result.nextCursor = null
```

Disposition: repair required.
