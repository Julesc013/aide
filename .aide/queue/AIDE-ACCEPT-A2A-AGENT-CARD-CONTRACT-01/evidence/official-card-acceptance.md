# Official AgentCard Acceptance

The accepted official AgentCard projection:

- pins target A2A specification release `1.0.0`;
- pins target A2A protocol version `1.0`;
- contains `supportedInterfaces`;
- uses a non-live `.invalid` HTTPS fixture URL: `https://aide.invalid/a2a/v1`;
- uses `protocolBinding: JSONRPC`;
- uses interface `protocolVersion: 1.0`;
- omits `provider`;
- omits legacy top-level `url`;
- omits `supportsAuthenticatedExtendedCard`;
- omits unsupported `stateTransitionHistory`;
- contains no AIDE governance fields;
- advertises no official skills: `skills: []`.

This is a fixture and projection acceptance only.
