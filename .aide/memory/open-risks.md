# AIDE Compact Open Risks

## Q09 Carry-Forward Risks

- Generated manifest source-fingerprint drift was present before Q09. Q09 may refresh it only through the existing Harness compile/write path, and evidence must state the final posture.
- Stale generated outputs can recur whenever source inputs change; generated artifacts remain downstream outputs, not canonical truth.
- Q00-Q03 and Q05/Q06 raw queue status nuance remains unresolved and intentionally visible.
- Token counts use approximate `chars / 4`; no exact tokenizer is included yet.
- No live provider billing integration or exact provider token ledger exists yet.
- No Gateway exists yet, so model routing, cache sharing, live redaction, and request-time budgets are not enforceable.
- No `.aide.local` boundary exists yet; local cache/state discipline is deferred to Q18.
- Context compiler remains deterministic and heuristic; no embeddings, semantic retrieval, or vector search exists yet.
- Verifier remains structural and path/ref oriented; no LLM judge or semantic diff validation exists yet.
- Golden tasks cover AIDE's token-saving workflow only; they do not prove arbitrary coding-task quality.
- Outcome Controller recommendations are heuristic and advisory; no automatic prompt/policy/route optimization exists.
- Router Profile remains deferred to Q17, cache/local-state boundary to Q18, and Gateway/provider/runtime/UI work remains deferred.
