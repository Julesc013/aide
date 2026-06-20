# Remaining Risks

- MCP server behavior is not implemented.
- No stdio or Streamable HTTP transport exists.
- No live resource, prompt, or tool serving exists.
- Authorization expectations are declared but no OAuth, credential,
  `PolicyDecision`, or `CapabilityGrant` implementation exists.
- The future `aide://interop/...` ReferenceID kind is advisory only; global
  ReferenceID authority remains unchanged.
- The MCP contract is not accepted by this build task; it requires independent
  check and later acceptance before becoming an accepted capability.
- Inherited report volume, generated-output provenance, stale-context,
  Reconciler, and queue readability warning debt remain unresolved.
