# Interop Exports Acceptance Report

`AIDE-ACCEPT-INTEROP-EXPORTS-01` accepts the first static interoperability
export preview capability with warnings.

Accepted capability:

```text
static_interop_export_previews
```

Accepted scope:

- deterministic static preview projection;
- manifest generation;
- SHA-256 artifact integrity binding;
- Markdown, JSON, and bounded YAML preview rendering;
- queue-authority and non-capability wording;
- inspection and report surfaces;
- drift inspection against the generated previews.

Not accepted:

- installation into live tool configuration paths;
- live MCP server, transport, resource serving, tool execution, or
  authentication;
- live A2A endpoint, delegation, authentication, or worker execution;
- provider/model/network calls;
- Host Contract, Host SDK, Dominium Bridge, Workbench, Commander, Service, or
  runtime;
- PatchTransaction approval or apply;
- branch/worktree automation, GitHub mutation, release, promotion, or target
  repository mutation.

Result: `ACCEPTED_WITH_WARNINGS`.
