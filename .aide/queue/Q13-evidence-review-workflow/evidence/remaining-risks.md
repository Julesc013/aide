# Q13 Remaining Risks

- Review packet quality depends on task-local evidence quality; Q13 does not infer missing evidence semantically.
- Q13 does not call GPT-5.5 or automate model review.
- Token counts remain approximate `chars / 4`; exact tokenizer and provider billing integration remain deferred.
- Q14 token ledger formalization is not implemented in Q13.
- Q15 golden-task quality proof is not implemented in Q13.
- Review-pack changed-file summaries are path/status based, not semantic diff analysis.
- Q12 verifier remains structural and heuristic.
- Gateway, router, cache boundary, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, and provider adapters remain deferred.
- Existing Harness warnings for generated manifest source-fingerprint drift and raw queue review-gate nuance remain visible.
