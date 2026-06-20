# AIDE-ACCEPT-MCP-SERVER-CONTRACT-01 Prompt Record

Create and process `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01` as an acceptance/consolidation task.

Use `.aide/queue/index.yaml` as canonical queue truth. Review the complete MCP source chain:

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01`
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01`
- `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`
- `AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01`

Accept only `minimal_mcp_server_contract` if the repaired contract is standards-aligned for the pinned MCP `2025-11-25` and JSON-RPC `2.0` subset, the original failed check is preserved, the repair check has zero material findings, all source task evidence is complete, and no superseding task exists.

Acceptance is limited to contract representation, deterministic projection, catalogues, JSON-RPC fixtures, refusal mappings, transport and authorization expectations, conformance expectations, structural validation, inspection, and reporting.

Acceptance must not imply live MCP server behavior, stdio or HTTP transport, endpoint binding, sessions, OAuth, authorization implementation, resource serving, prompt serving, tool execution, worker execution, provider/model/network calls, repository mutation, A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service, release, or production readiness.

Stop at `needs_review`. If accepted, recommend exactly `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`.
