# Q17 Remaining Risks

- Route heuristics are deterministic and conservative, but they are not semantic
  model judgement.
- Provider capability records are advisory metadata only; Q17 does not verify
  current provider availability, pricing, features, quotas, or model behavior.
- No provider calls, model calls, Gateway, proxy, Runtime, Service, Commander,
  UI, Mobile, MCP/A2A, host/app implementation, or local model setup exists.
- No exact tokenizer is implemented; token sizes still use chars divided by 4.
- No exact provider billing, hidden reasoning-token accounting, or cached-token
  accounting exists.
- No cache/local-state boundary exists yet; Q18 should define what can be
  cached, where local state may live, and what must stay uncommitted.
- Signal parsing is local and may be conservative when reports are missing or
  unusually shaped.
- Failed verifier or golden-task gates affect route decisions, but Q17 does not
  repair those gates automatically.
- Review packets remain dependent on evidence quality and Q12 structural
  verifier coverage; no LLM-as-judge is introduced.
- Existing generated manifest fingerprint drift and raw queue review-gate nuance
  remain visible warnings rather than being silently normalized.
