# CLI Boundary Review

Required command results:

- `mcp-server-contract status`: `PASS_WITH_WARNINGS`
- `mcp-server-contract project`: `PASS_WITH_WARNINGS`
- `mcp-server-contract validate`: `PASS_WITH_WARNINGS`

Unsupported command probes returned non-zero for:

- `start`
- `serve`
- `listen`
- `connect`
- `call`
- `install`
- `authorize`

No execution-like CLI behavior is available.
