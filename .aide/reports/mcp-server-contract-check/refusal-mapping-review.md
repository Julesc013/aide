# Refusal Mapping Review

Refusal fixtures reviewed:

- runtime not implemented
- resource not found
- required capability unavailable
- unsupported protocol version

Each is a JSON-RPC error response. Custom server error codes are used for AIDE
application/server refusals.

Material finding `MCP-CHECK-002` applies because the resource-not-found fixture
uses `-32043` while claiming the MCP resource-not-found mapping, whose pinned
code is `-32002`.
