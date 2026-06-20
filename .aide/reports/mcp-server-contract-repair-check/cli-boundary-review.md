# CLI Boundary Review

The supported MCP contract commands returned `PASS_WITH_WARNINGS`:

- `mcp-server-contract status`
- `mcp-server-contract project`
- `mcp-server-contract validate`

Unsupported operations fail closed:

- `start`
- `serve`
- `listen`
- `connect`
- `call`
- `install`
- `authorize`

No server, transport, resource serving, prompt serving, tool invocation,
network call, credential resolution, or repository mutation occurred.
