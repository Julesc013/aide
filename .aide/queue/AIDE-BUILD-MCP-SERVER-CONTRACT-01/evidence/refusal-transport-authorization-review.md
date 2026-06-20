# Refusal, Transport, And Authorization Review

Typed refusal mappings include:

- `MCP_RUNTIME_NOT_IMPLEMENTED`
- `MCP_RESOURCE_NOT_FOUND`
- `MCP_REQUIRED_CAPABILITY_UNAVAILABLE`
- `AIDE_POLICY_OR_GRANT_UNAVAILABLE`
- `MCP_UNSUPPORTED_PROTOCOL_VERSION`

Transport profiles are declared for:

- `stdio`
- `streamable_http`

Each transport records `implementation_status: not_implemented`.

Authorization records:

- `authorization_supported_by_contract: true`
- `authorization_implemented: false`

MCP transport authorization remains distinct from future AIDE
`PolicyDecision` and `CapabilityGrant` authority. OAuth, client registration,
token issuance/parsing/storage, credential resolution, and authorization-server
discovery are not implemented.
