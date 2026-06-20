# CLI Boundary Review

Supported MCP commands returned `PASS_WITH_WARNINGS`:

- `mcp-server-contract status`
- `mcp-server-contract project`
- `mcp-server-contract validate`

Unsupported operation probe passed:

```text
unsupported_probe PASS commands=start,serve,listen,connect,call,install,authorize
```

Unsupported execution commands fail closed.
