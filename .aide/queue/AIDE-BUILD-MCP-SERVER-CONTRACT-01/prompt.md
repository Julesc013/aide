# AIDE-BUILD-MCP-SERVER-CONTRACT-01

Create and process `AIDE-BUILD-MCP-SERVER-CONTRACT-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything.

Build the first minimal, deterministic, contract-only MCP projection for AIDE,
pinned to MCP protocol version `2025-11-25` and JSON-RPC version `2.0`.

Implement only:

- schema;
- helper/projection/validation module;
- thin AIDE Lite status/project/validate dispatch;
- deterministic contract/catalogue/fixture/report projections;
- focused tests;
- task-local evidence and next-task prompt.

Do not start a server, implement transport/authentication, serve resources,
invoke tools, serve prompts, call providers/models/network services, dispatch
workers, apply patches, mutate branches/worktrees/GitHub/target repositories,
or implement A2A, Host Contract, Dominium Bridge, Workbench, Runtime, Service,
scheduler, leases, supervisor, release, or promotion behavior.

Stop at `needs_review` and recommend only
`AIDE-CHECK-MCP-SERVER-CONTRACT-01`.
