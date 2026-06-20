# Tool Refusal Review

`tools-call-refusal.json` is a JSON-RPC error response. It preserves the refused
tool as `error.data.tool_name: aide.status`, reports
`reason_code: MCP_RUNTIME_NOT_IMPLEMENTED`, and does not fabricate a tool
result.

No tool execution occurred. Unsupported CLI operations such as `start`, `serve`,
`listen`, `connect`, `call`, `install`, and `authorize` fail closed.
