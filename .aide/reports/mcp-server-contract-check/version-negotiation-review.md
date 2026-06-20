# Version Negotiation Review

The persisted target protocol version is exactly `2025-11-25`.

The initialize request uses `2025-11-25`, and the initialize result returns
`2025-11-25`. The supported protocol version list contains only
`2025-11-25`.

The unsupported-version fixture is structurally a JSON-RPC error response and
does not imply live negotiation occurred.

No backward compatibility with other MCP versions is claimed.
