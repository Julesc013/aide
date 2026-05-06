# AIDE Compact Open Risks

## Q09 Carry-Forward Risks

- Generated manifest source-fingerprint drift was present before Q09. Q09 may refresh it only through the existing Harness compile/write path, and evidence must state the final posture.
- Stale generated outputs can recur whenever source inputs change; generated artifacts remain downstream outputs, not canonical truth.
- Q00-Q03 and Q05/Q06 raw queue status nuance remains unresolved and intentionally visible.
- Token counts use approximate `chars / 4`; no exact tokenizer is included yet.
- No live provider billing integration or exact provider token ledger exists yet.
- Q19 adds a local/report-only Gateway skeleton, but no production Gateway, provider adapter, live request forwarding, authentication, authorization, live redaction, or request-time budget enforcement exists yet.
- Q18 defines the .aide.local/ boundary and cache-key metadata, but no live cache, provider response cache, semantic cache, or runtime cache service exists yet.
- Context compiler remains deterministic and heuristic; no embeddings, semantic retrieval, or vector search exists yet.
- Verifier remains structural and path/ref oriented; no LLM judge or semantic diff validation exists yet.
- Golden tasks cover AIDE's token-saving workflow only; they do not prove arbitrary coding-task quality.
- Outcome Controller recommendations are heuristic and advisory; no automatic prompt/policy/route optimization exists.
- Router Profile route decisions are deterministic advisory metadata only; no live provider availability, current pricing, Gateway execution, or model routing exists.
- Cache-key reports are metadata only and do not prove stale content is safe to reuse.
- Provider/runtime/UI work remains deferred, and Q19 Gateway endpoints are status-only.
