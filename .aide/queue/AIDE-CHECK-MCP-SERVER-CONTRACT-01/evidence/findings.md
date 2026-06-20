# Findings

`FAILED_VALIDATION`

Material findings:

1. `MCP-CHECK-001`: null cursor fields in six list request/result fixtures.
2. `MCP-CHECK-002`: `resource-not-found-refusal.json` uses `-32043` instead of
   pinned resource-not-found code `-32002`.

Recommended repair task:

`AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`
