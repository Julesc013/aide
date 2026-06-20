# Refusal Mapping Acceptance

Accepted refusal mapping facts:

- MCP resource-not-found uses `-32002`;
- runtime-not-implemented keeps custom code `-32040`;
- unsupported-protocol-version keeps custom code `-32041`;
- required-capability-unavailable keeps custom code `-32042`;
- reason codes remain bounded and explicit.

No PolicyDecision or CapabilityGrant record is fabricated by this projection.
