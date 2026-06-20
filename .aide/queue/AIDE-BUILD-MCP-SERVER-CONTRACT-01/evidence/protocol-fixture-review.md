# Protocol And Fixture Review

The contract pins:

- MCP target protocol version: `2025-11-25`
- supported protocol versions: `2025-11-25`
- JSON-RPC version: `2.0`
- backward compatibility claimed: `false`
- forward compatibility claimed: `false`

Generated fixtures under `.aide/interop/mcp/fixtures/` cover:

- initialize request/result
- initialized notification
- resources/list request/result
- resources/read request/result
- tools/list request/result
- tools/call refusal
- prompts/list request/result
- unsupported protocol-version refusal
- required-capability refusal
- resource-not-found refusal

All fixtures are static JSON-RPC examples. They are not connected to a live
dispatcher, transport, server, endpoint, resource reader, prompt renderer, or
tool execution path.
