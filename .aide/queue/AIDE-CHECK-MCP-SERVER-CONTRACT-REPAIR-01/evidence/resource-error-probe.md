# Resource Error Probe

Independent fixture inspection verified:

- `resource-not-found-refusal.json` is JSON-RPC `2.0`.
- It has response ID `9`.
- `error.code` is exactly `-32002`.
- `error.message` is resource-not-found specific.
- `error.data.reason_code` is `MCP_RESOURCE_NOT_FOUND`.
- `error.data.uri` is `aide://workunit/not-found`.

Temporary mutation of the resource-not-found error code back to `-32043`
fails validation.
