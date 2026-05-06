# Q16 Safety Boundary

## Advisory-Only Boundary

Q16 is an observer and recommender. It may read deterministic local reports and write controller outputs under `.aide/controller/**`; it must not apply recommendations automatically.

## Explicitly Forbidden

- automatic prompt mutation
- automatic policy mutation
- automatic route mutation
- automatic context strategy rewrite
- automatic generated-artifact rewrite outside explicit Q16 deliverables
- provider calls
- model calls
- network calls
- Gateway or proxy behavior
- Runtime, Service, Commander, UI, Mobile, MCP/A2A, or host implementation
- autonomous loops

## Allowed Outputs

- `.aide/controller/outcome-ledger.jsonl`
- `.aide/controller/latest-outcome-report.md`
- `.aide/controller/latest-recommendations.md`
- Q16 queue evidence and docs

## Promotion Rule

Any recommendation must be implemented by a future queue item or explicit human approval. Before promotion, the work must rerun verifier checks, review-packet generation, token ledger checks, and golden tasks.
