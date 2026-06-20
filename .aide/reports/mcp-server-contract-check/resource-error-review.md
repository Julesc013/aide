# Resource Error Review

The pinned prompt identifies MCP resource-not-found as error code `-32002`.

Observed fixture:

```text
.aide/interop/mcp/fixtures/resource-not-found-refusal.json
error.code: -32043
error.data.reason_code: MCP_RESOURCE_NOT_FOUND
```

Because the fixture names and labels this as the MCP resource-not-found mapping,
the code mismatch is a material standards-alignment defect.
