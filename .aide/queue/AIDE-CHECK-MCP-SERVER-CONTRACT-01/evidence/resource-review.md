# Resource Review

Resource count: `10`

All resource URIs are unique, bounded `aide://` projections, and remain
unserved.

Material failure:

```text
.aide/interop/mcp/fixtures/resource-not-found-refusal.json
actual error.code: -32043
expected error.code: -32002
```

The fixture labels the condition as MCP resource not found, so this is a
standards-alignment defect.
