# Boundary Review

The checked preview artifacts preserve the intended boundary:

- `AGENTS.md.preview`, `CLAUDE.md.preview`, and
  `copilot-instructions.md.preview` point back to queue truth and task-local
  evidence.
- `aider.conf.yml.preview` is explicitly not an active model-call
  configuration.
- `mcp-manifest.preview.json` records `server_implemented: false`.
- `a2a-agent-card.preview.json` records `endpoint_implemented: false`.
- `.aide/interop/exports/manifest.json` records explicit non-capabilities as
  `false`.

No preview artifact claims active runtime, provider/model call, worker
execution, apply, admission, trust, release, or target mutation capability.
