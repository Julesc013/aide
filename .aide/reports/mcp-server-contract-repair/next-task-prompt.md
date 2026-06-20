# AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01

Independently recheck the MCP server contract repair.

Verify that:

- `AIDE-CHECK-MCP-SERVER-CONTRACT-01` remains preserved with
  `FAILED_VALIDATION`;
- `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01` completed at `needs_review` with
  `PASS_WITH_WARNINGS`;
- no MCP paginated fixture emits `cursor: null` or `nextCursor: null`;
- present cursor and nextCursor values are strings;
- `resource-not-found-refusal.json` uses `-32002`;
- custom AIDE refusal codes remain distinct;
- focused tests and MCP validation pass;
- projection is deterministic;
- accepted Interop Export artifacts and failed-check reports are unchanged;
- no live MCP runtime, transport, authorization, serving, invocation, provider,
  worker, network, A2A, Host Contract, Dominium Bridge, Workbench, service,
  mutation, release, or promotion behavior was added.

If the repair passes, recommend `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01` or the
live queue's accepted resume equivalent. If it fails, recommend one bounded
repair task.
