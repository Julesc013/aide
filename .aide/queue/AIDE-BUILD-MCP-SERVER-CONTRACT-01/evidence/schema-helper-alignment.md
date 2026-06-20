# Schema And Helper Alignment

- Schema path:
  `.aide/protocol/aide-mcp-server-contract.schema.json`
- Helper path:
  `core/interop/mcp_server_contract.py`
- CLI path:
  `.aide/scripts/aide_lite.py`

The helper projects `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
The schema title is `AIDE Minimal MCP Server Contract`, and the helper
validates the kind `McpServerContract`.

Validation report:

- `.aide/reports/mcp-server-contract/validation.json`
- `schema_helper_alignment_checked: true`
- `schema_helper_alignment_status: PASS`
- `validation_status: PASS_WITH_WARNINGS`

The global ReferenceID scheme was not broadened. The future
`aide://interop/mcp-server-contract-v0` identity is recorded as advisory
metadata and warning debt.
