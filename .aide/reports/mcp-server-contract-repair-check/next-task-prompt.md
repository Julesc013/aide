# AIDE-ACCEPT-MCP-SERVER-CONTRACT-01

Create and process `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

Do not execute acceptance unless:

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01` exists with result `PASS` or
  `PASS_WITH_WARNINGS` and `missing_evidence: 0`;
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01` remains preserved with
  `FAILED_VALIDATION`;
- `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01` exists with result `PASS` or
  `PASS_WITH_WARNINGS` and `missing_evidence: 0`;
- `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01` exists with result `PASS` or
  `PASS_WITH_WARNINGS`, `missing_evidence: 0`, and zero material findings;
- no unresolved MCP repair task or superseding MCP task exists.

Acceptance scope must be limited to the contract-only,
projection-only `minimal_mcp_server_contract` capability. Acceptance must not
start MCP, implement stdio or Streamable HTTP, bind endpoints, implement
authorization, serve resources/prompts, execute tools, dispatch workers, call
providers/models/network services, implement A2A, Host Contract, Dominium
Bridge, Workbench, Runtime, Service, apply PatchTransactions, mutate target
repositories, create branches/worktrees, mutate GitHub, release, promote, or
claim production readiness.

If accepted, recommend:

```text
AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01
```
