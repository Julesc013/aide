# Legacy Field Recheck

PASS.

The official card no longer includes:

- top-level `url`;
- top-level `protocolVersion`;
- `preferredTransport`;
- `additionalInterfaces`;
- top-level `supportsAuthenticatedExtendedCard`;
- top-level `supportsExtendedAgentCard`.

Extended-card support is represented only as `capabilities.extendedAgentCard: false`.
