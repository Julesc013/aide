# Interop Projection Report

`AIDE-BUILD-INTEROP-EXPORTS-01` projects the accepted current AIDE operating
boundary into static interop previews for future external tool surfaces.

The projection is intentionally narrow:

- guidance previews for agent-facing, Claude-facing, Copilot-facing, and Aider
  style consumers;
- preview JSON for future MCP and A2A discovery;
- a manifest recording artifact hashes and explicit non-capabilities.

The projection does not create:

- a live MCP server;
- a live A2A endpoint;
- a Host Contract or Host SDK;
- Dominium Bridge conformance;
- Workbench or Commander behavior;
- provider, model, Gateway, GitHub, or network calls;
- worker dispatch;
- patch application, approval, rollback, admission, or trust;
- branch/worktree automation;
- release, promotion, or target-repository mutation.

Result: `PASS_WITH_WARNINGS`.

Recommended next task: `AIDE-CHECK-INTEROP-EXPORTS-01`.
