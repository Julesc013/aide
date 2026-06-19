# AIDE-BUILD-INTEROP-EXPORTS-01

Create and process `AIDE-BUILD-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the accepted
ContextPack v2 route unless live queue evidence has superseded it.

Build only static, deterministic, report-only interop export previews after
ContextPack v2 acceptance. Do not implement live MCP or A2A servers, provider
or model calls, worker dispatch, runtime behavior, Host Contract, Dominium
Bridge conformance, Workbench, PatchTransaction apply, branch or worktree
automation, GitHub mutation, release, or target repository mutation.

Expected static preview surfaces may include:

- `AGENTS.md.preview`
- `CLAUDE.md.preview`
- `copilot-instructions.md.preview`
- aider config preview
- MCP manifest preview
- A2A agent card preview

Stop at `needs_review`.
