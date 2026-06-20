# CLI Boundary Review

Required commands were probed:

- `mcp-server-contract status`: `PASS_WITH_WARNINGS`
- `mcp-server-contract project`: `PASS_WITH_WARNINGS`
- `mcp-server-contract validate`: `PASS_WITH_WARNINGS`

Unsupported operations fail closed:

- `start`
- `serve`
- `listen`
- `connect`
- `call`
- `install`
- `authorize`

No server started, socket bound, endpoint contacted, resource served, tool
invoked, prompt served, credential resolved, worker dispatched, model called,
or repository mutated.
