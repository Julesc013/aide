# AIDE-ACCEPT-INTEROP-EXPORTS-01

Create and process `AIDE-ACCEPT-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

This is an acceptance/consolidation task for static interoperability export
previews after `AIDE-BUILD-INTEROP-EXPORTS-01` and
`AIDE-CHECK-INTEROP-EXPORTS-01`.

If accepted, record only:

```text
static_interop_export_previews
```

Acceptance is limited to deterministic static preview generation, manifest
generation, content hashing, structural validation, inspection, review, and
reporting.

Acceptance must not imply live instruction installation, live MCP, live A2A,
external tool integration, Host Contract, Dominium Bridge, Workbench, worker
execution, provider/model/network calls, runtime behavior, PatchTransaction
application, branch/worktree automation, GitHub mutation, release, promotion,
or target repository mutation.

Stop at `needs_review`.
