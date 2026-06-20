# AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01

Repair only the two material MCP standards-alignment findings from
`AIDE-CHECK-MCP-SERVER-CONTRACT-01`:

1. optional pagination fields must be omitted when absent and must be strings
   when present;
2. the MCP resource-not-found fixture must use `-32002`.

Preserve the failed check as historical evidence. Strengthen tests and
validation, regenerate only affected MCP contract fixtures and reports, keep MCP
projection-only, and stop at `needs_review`.

Recommended next task:

```text
AIDE-CHECK-MCP-SERVER-CONTRACT-REPAIR-01
```
