# AIDE Interop Export Previews

This directory contains static, deterministic preview artifacts for external
tool guidance and interop discovery.

These files are generated review candidates. They are not canonical queue,
protocol, evidence, runtime, MCP, A2A, provider, worker, GitHub, release, or
target-repository authority.

Current preview set:

- `AGENTS.md.preview`
- `CLAUDE.md.preview`
- `copilot-instructions.md.preview`
- `aider.conf.yml.preview`
- `mcp-manifest.preview.json`
- `a2a-agent-card.preview.json`

Every preview preserves the same boundary: read repository truth from the live
AIDE queue and evidence surfaces, do not execute workers, do not call providers
or networks, and do not mutate repositories unless a later reviewed queue task
explicitly authorizes that behavior.
