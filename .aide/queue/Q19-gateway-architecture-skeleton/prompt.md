# Q19 Implementation Prompt

Implement Q19 Gateway Architecture and Skeleton as a bounded AIDE queue phase.

Q19 depends on Q09-Q18 and must not implement provider calls, model calls,
outbound network calls, real Gateway proxy forwarding, OpenAI-compatible
forwarding, Anthropic-compatible forwarding, Runtime, UI, Commander, MCP, A2A,
semantic cache, or autonomous execution.

Required result:

- Gateway policy under `.aide/policies/gateway.yaml`.
- Gateway architecture/status artifacts under `.aide/gateway/`.
- Core stdlib skeleton under `core/gateway/`.
- AIDE Lite `gateway status`, `gateway endpoints`, `gateway smoke`, and optional
  localhost-only `gateway serve` behavior.
- Compact health/status/route/summaries/version responses.
- Generated latest Gateway status reports.
- Generated Q20 compact task packet for `Implement Q20 Provider Adapter v0`.
- Evidence, tests, docs, and review-gated status.

All outputs must avoid raw prompt bodies, raw response bodies, secrets, provider
keys, `.aide.local/` contents, provider/model calls, and outbound network calls.
