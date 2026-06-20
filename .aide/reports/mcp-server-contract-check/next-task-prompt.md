# AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01

Repair only the material defects found by
`AIDE-CHECK-MCP-SERVER-CONTRACT-01`.

Required baseline:

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01` exists and remains preserved.
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01` exists with result
  `FAILED_VALIDATION`.
- Check evidence reports `missing_evidence: 0`.
- The material findings are:
  1. list request/result fixtures emit `null` for `cursor` or `nextCursor`;
  2. `resource-not-found-refusal.json` uses `-32043` instead of `-32002`.

Repair scope:

- Replace absent pagination cursor fields with omission, or strings where
  intentionally present.
- Align the resource-not-found fixture with the pinned MCP resource-not-found
  code `-32002`, or explicitly relabel it as a separate AIDE application
  refusal and add a correct MCP resource-not-found fixture.
- Update focused tests and deterministic reports as needed.

Non-goals:

- do not accept MCP;
- do not erase the failed check;
- do not start a live server;
- do not implement stdio, Streamable HTTP, authorization, serving, tool
  execution, worker execution, provider/model/network calls, A2A, Host
  Contract, Dominium Bridge, Workbench, runtime, branch/worktree automation,
  release, promotion, or target mutation.

Expected result: `PASS_WITH_WARNINGS`

Recommended next task after repair: `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`
