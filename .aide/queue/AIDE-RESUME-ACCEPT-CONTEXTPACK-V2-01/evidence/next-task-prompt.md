# AIDE-BUILD-INTEROP-EXPORTS-01

Create and process `AIDE-BUILD-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Build only static,
deterministic, report-only interop export previews after ContextPack v2
acceptance.

Do not implement live MCP or A2A servers, provider/model calls, worker dispatch,
runtime behavior, patch application, branch/worktree automation, GitHub
mutation, release, or target repository mutation.

Stop at `needs_review`.
