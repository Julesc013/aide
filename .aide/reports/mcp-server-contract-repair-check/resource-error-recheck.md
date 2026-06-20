# Resource Error Recheck

`resource-not-found-refusal.json` is a JSON-RPC error response with:

- `jsonrpc: "2.0"`
- `id: 9`
- `error.code: -32002`
- `error.message: "Resource not found"`
- `error.data.reason_code: "MCP_RESOURCE_NOT_FOUND"`
- `error.data.uri: "aide://workunit/not-found"`

No secret or internal implementation detail was found in the resource-not-found
fixture.
