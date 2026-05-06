# AIDE Compact Open Risks

## Q09 Carry-Forward Risks

- Generated manifest source-fingerprint drift was present before Q09. Q09 may refresh it only through the existing Harness compile/write path, and evidence must state the final posture.
- Stale generated outputs can recur whenever source inputs change; generated artifacts remain downstream outputs, not canonical truth.
- Q00-Q03 and Q05/Q06 raw queue status nuance remains unresolved and intentionally visible.
- Token counts use approximate `chars / 4`; no exact tokenizer is included yet.
- No live provider billing integration or exact provider token ledger exists yet.
- No Gateway exists yet, so model routing, cache sharing, live redaction, and request-time budgets are not enforceable.
- No `.aide.local` boundary exists yet; local cache/state discipline is deferred to Q18.
- No context compiler beyond Q09 snapshot exists yet; exact repo map, test map, and line-range retrieval remain Q11 work.
- No verifier/evidence gate beyond Q09 basic validation exists yet; Q12 is still required.
- No golden task quality proof exists yet; Q15 is still required before claiming token reduction preserves quality across recurring tasks.
