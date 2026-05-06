# Q12 Prompt: Verifier v0

Implement Q12 as a bounded queue phase.

## Objective

Build deterministic, repo-local verifier behavior so future tasks can mechanically check compact task packets, evidence packets, file references, line refs, changed-file scope, adapter drift, context packet shape, token warnings, and obvious secret risks before premium-model review.

## Required Outputs

- `.aide/policies/verification.yaml`
- `.aide/verification/evidence-packet.template.md`
- `.aide/verification/review-packet.template.md`
- `.aide/verification/diff-scope-policy.yaml`
- `.aide/verification/file-reference-policy.yaml`
- `.aide/verification/secret-scan-policy.yaml`
- `.aide/verification/latest-verification-report.md`
- AIDE Lite `verify` behavior
- `.aide/context/latest-task-packet.md` for Q13
- Tests, docs, evidence, and Q12 status `needs_review`

## Boundaries

Do not implement Gateway, providers, routing, local model setup, embeddings, vector search, exact tokenization, provider billing, Q13 automated review, Q14 token ledger, Q15 golden tasks, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, LLM-as-judge, automatic repair, or autonomous loops.
