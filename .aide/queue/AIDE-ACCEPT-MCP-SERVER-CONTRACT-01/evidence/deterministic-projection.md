# Deterministic Projection

Determinism evidence accepted from the build, repair, and repair-check chain:

- MCP validate reports `deterministic_projection: true`.
- MCP validate reports `source_artifacts_mutated: false`.
- Repair-check evidence confirms repeated projection bytes matched.
- Fixture index hashes are stable and match actual fixture bytes.

This acceptance did not run `mcp-server-contract project` as an acceptance mutation step.
