# Historical Failure Preservation

The original independent check remains `FAILED_VALIDATION`.

Preserved material findings:

- `MCP-CHECK-001`: list pagination fixtures emitted explicit `null` cursor or `nextCursor` values.
- `MCP-CHECK-002`: `resource-not-found-refusal.json` used `-32043` rather than the pinned MCP resource-not-found code `-32002`.

The acceptance records the failed check as historical evidence and does not rewrite it as passed.
