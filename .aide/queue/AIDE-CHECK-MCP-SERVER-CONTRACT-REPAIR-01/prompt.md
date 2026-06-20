# AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01

Independently recheck the bounded MCP pagination and resource-error repair.

Verify:

- absent cursor and nextCursor fields are omitted;
- present cursor and nextCursor values are strings;
- temporary invalid cursor regressions fail validation;
- `resource-not-found-refusal.json` uses `-32002`;
- custom AIDE refusal codes remain unchanged;
- JSON-RPC fixture shape remains valid;
- projection is deterministic;
- source and historical evidence are unchanged;
- no live MCP runtime or forbidden operation occurred.

If the repair passes, recommend:

```text
AIDE-ACCEPT-MCP-SERVER-CONTRACT-01
```
