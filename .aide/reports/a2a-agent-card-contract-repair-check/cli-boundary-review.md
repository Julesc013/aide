# CLI Boundary Review

PASS.

Supported commands:

- `a2a-agent-card-contract status`: PASS_WITH_WARNINGS.
- `a2a-agent-card-contract project`: PASS_WITH_WARNINGS.
- `a2a-agent-card-contract validate`: PASS_WITH_WARNINGS.

Unsupported runtime verbs fail closed with exit code 2: start, serve, register, publish, discover, send, delegate, submit, stream, subscribe, cancel, authenticate, and connect.
