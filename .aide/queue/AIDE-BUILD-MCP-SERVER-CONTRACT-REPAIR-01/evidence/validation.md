# Validation

Final validation disposition:

- `git status --short --branch`: repair diff only.
- `git diff --check`: exit 0; retained pre-existing line-ending warning for
  `.aide/queue/index.yaml`.
- `git diff --cached --check`: exit 0.
- Python compilation: pass.
- focused MCP tests: 65 passed.
- `mcp-server-contract status`: `PASS_WITH_WARNINGS`.
- `mcp-server-contract project`: `PASS_WITH_WARNINGS`.
- `mcp-server-contract validate`: `PASS_WITH_WARNINGS`.
- `context-pack-v2 status`: `PASS_WITH_WARNINGS`.
- `adapter-manifest validate`: `PASS_WITH_WARNINGS`.
- `patch-transaction validate`: `PASS_WITH_WARNINGS`.
- `reference-id validate`: `PASS_WITH_WARNINGS`.
- `event-record validate`: `PASS_WITH_WARNINGS`.
- `capability-manifest validate`: `PASS_WITH_WARNINGS`.
- `conformance-profile validate`: `PASS_WITH_WARNINGS`.
- `conformance-result validate`: `PASS_WITH_WARNINGS`.
- `okf validate`: `PASS_WITH_WARNINGS`.
- `reconciler validate`: `PASS_WITH_WARNINGS`.
- repair task inspect/evidence: `missing_evidence: 0`.
- JSON parsing for MCP fixtures and MCP repair/contract JSON reports: pass,
  33 files parsed.
- independent fixture probe: pass, 15 fixtures checked.
- unsupported MCP execution command probe: pass; `start`, `serve`, `listen`,
  `connect`, `call`, `install`, and `authorize` fail closed.
- repeated projection byte comparison: pass, 45 files compared.
- broad `aide_lite.py validate`: `PASS`.
- changed-file secret-like scan: 0 material findings after classifying the
  existing MCP test sentinel strings as non-secret.

No live MCP runtime, transport, authorization, serving, invocation, provider,
worker, network, branch/worktree, target mutation, release, or promotion
behavior occurred.
