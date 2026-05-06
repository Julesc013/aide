# Q20 Implementation Prompt

Implement Q20 Provider Adapter v0 as a bounded AIDE queue phase.

Q20 depends on Q09-Q19 and must not implement live provider calls, model calls,
outbound network calls, real Gateway proxy forwarding, OpenAI-compatible
forwarding, Anthropic-compatible forwarding, provider probes, credential setup,
local model setup, Runtime, UI, Commander, MCP, A2A, semantic cache, or
autonomous execution.

Required result:

- Provider adapter policy under `.aide/policies/provider-adapters.yaml`.
- Provider metadata artifacts under `.aide/providers/`.
- Core stdlib provider contracts under `core/providers/`.
- AIDE Lite `provider list`, `provider status`, `provider validate`,
  `provider contract`, and `provider probe --offline`.
- Compact latest provider status JSON and Markdown reports.
- Gateway status integration for provider metadata readiness only.
- Advisory route metadata integration only; no route execution.
- Generated Q21 compact task packet for `Implement Q21 Existing Tool Adapter
  Compiler v0`.
- Evidence, tests, docs, and review-gated status.

All outputs must avoid provider credentials, API keys, raw prompt bodies, raw
response bodies, `.aide.local/` contents, live provider calls, model calls,
outbound network calls, and Gateway forwarding.
