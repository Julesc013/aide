# Custom Refusal Preservation

Custom AIDE refusal codes remain unchanged:

- `tools-call-refusal.json`: `-32040`, `MCP_RUNTIME_NOT_IMPLEMENTED`
- `protocol-version-refusal.json`: `-32041`,
  `MCP_UNSUPPORTED_PROTOCOL_VERSION`
- `capability-refusal.json`: `-32042`,
  `MCP_REQUIRED_CAPABILITY_UNAVAILABLE`

The repair did not collapse these application refusals into resource-not-found.
