# Schema Helper Alignment

The new schema is envelope-shaped:

- `apiVersion`
- `kind`
- `metadata`
- `spec`
- `status`

`a2a-agent-card-contract validate` reports:

- schema exists: `true`
- schema file parsed: `true`
- schema/helper alignment checked: `true`
- schema/helper alignment status: `PASS`
- contract valid: `true`

The helper preserves additive optional fields but fails closed for unknown
required AIDE capabilities and runtime/status facts that would imply execution.
