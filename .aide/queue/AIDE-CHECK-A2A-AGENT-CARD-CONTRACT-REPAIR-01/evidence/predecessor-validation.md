# Predecessor Validation

Predecessor checks run:

- `mcp-server-contract validate`: PASS_WITH_WARNINGS.
- `context-pack-v2 status`: PASS_WITH_WARNINGS.
- `adapter-manifest validate`: PASS_WITH_WARNINGS.
- `patch-transaction validate`: PASS_WITH_WARNINGS.
- `reference-id validate`: PASS_WITH_WARNINGS.
- `event-record validate`: PASS_WITH_WARNINGS.
- `capability-manifest validate`: PASS_WITH_WARNINGS.
- `conformance-profile validate`: PASS_WITH_WARNINGS.
- `conformance-result validate`: PASS_WITH_WARNINGS.
- `okf validate`: PASS_WITH_WARNINGS.
- `reconciler validate`: PASS_WITH_WARNINGS.

Warnings remain expected for intentionally absent runtime, policy, admission, trust, provider, worker, network, host, and mutation behavior.
