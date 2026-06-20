# Next Task Prompt

Next serialized task:

```text
AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01
```

Repair only:

- null `cursor` and `nextCursor` fields in MCP list fixtures;
- the resource-not-found MCP error-code mismatch.

Do not begin acceptance until the repair and independent repair check pass.
