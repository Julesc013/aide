# JSON-RPC Regression Review

All MCP fixtures were parsed and checked for:

- `jsonrpc: "2.0"`;
- valid request or notification shape;
- initialized notification without an ID;
- responses containing exactly one of `result` or `error`;
- aligned request/response IDs;
- integer error codes;
- string error messages;
- object error data where present;
- initialization result protocol version `2025-11-25`.

No JSON-RPC regression was found.
