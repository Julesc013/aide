# AIDE-BUILD-MCP-SERVER-CONTRACT-01

Create and process `AIDE-BUILD-MCP-SERVER-CONTRACT-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

Goal: build a contract-only MCP server description for AIDE interop after
`static_interop_export_previews` acceptance.

The task must be contract-only. It must not start a server, expose live
resources, register live tools, create transport, authenticate clients, call
providers/models/network services, dispatch workers, apply patches, mutate
branches/worktrees, mutate GitHub, publish releases, or mutate target
repositories.

Preserve these non-capabilities:

- no live MCP server;
- no MCP transport;
- no MCP authentication;
- no MCP tool execution;
- no MCP resource serving;
- no live A2A endpoint;
- no Host Contract;
- no Dominium Bridge;
- no Workbench;
- no runtime or Service;
- no provider/model/network calls;
- no PatchTransaction approval or apply.

Stop at `needs_review`.
