# Determinism And Immutability

MCP projection and validation returned:

- `mcp-server-contract status`: `PASS_WITH_WARNINGS`
- `mcp-server-contract project`: `PASS_WITH_WARNINGS`
- `mcp-server-contract validate`: `PASS_WITH_WARNINGS`
- `deterministic_projection: true`
- `source_artifacts_mutated: false`

After projection and validation, `git status --short --branch` still reported a
clean worktree before check-only outputs were written.
