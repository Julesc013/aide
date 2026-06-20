# JSON-RPC Regression

JSON-RPC regression check passed:

```text
jsonrpc_regression_check PASS fixtures=15
```

Checked:

- `jsonrpc: "2.0"`;
- valid request/notification shape;
- notifications without IDs;
- responses with exactly one of `result` or `error`;
- aligned request/response IDs;
- integer error codes;
- string error messages;
- structurally valid error data;
- initialization result protocol version `2025-11-25`.
