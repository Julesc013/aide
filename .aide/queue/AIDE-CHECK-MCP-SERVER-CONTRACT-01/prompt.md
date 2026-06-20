# AIDE-CHECK-MCP-SERVER-CONTRACT-01

Independent check of the minimal contract-only MCP projection.

Use `.aide/queue/index.yaml` as canonical queue truth. Verify that
`AIDE-BUILD-MCP-SERVER-CONTRACT-01` exists, is complete at `needs_review`, has
result `PASS` or `PASS_WITH_WARNINGS`, has `missing_evidence: 0`, records build
commit `c8a143f76af585ae3a0cc3004fb5278c57f264e0` at live HEAD or an ancestor,
and recommends this check. Preserve `AIDE-ACCEPT-INTEROP-EXPORTS-01` as accepted.

Check the pinned contract subset:

- MCP protocol version: `2025-11-25`
- JSON-RPC version: `2.0`
- initialization before normal operations
- capability negotiation and client/server capability direction
- Resources, Tools, and Prompts as static server-feature projections
- stdio and Streamable HTTP expectations as not implemented
- authorization expectations as future contract concerns only

Do not download MCP schemas or SDKs. Do not start a server, launch subprocesses,
bind sockets, make network requests, serve resources, execute tools, serve
prompts, implement authorization, mutate repositories, or repair the build.

If no material finding exists, recommend `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`.
If a repairable material finding exists, recommend exactly
`AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`.
