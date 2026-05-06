# Q16 Remaining Risks

## Remaining Risks

- Recommendations are heuristic and local; they do not replace human or GPT-5.5 review.
- Signal parsing is conservative and may miss semantic quality issues.
- Golden tasks cover AIDE's token-saving substrate, not arbitrary coding-task correctness.
- Verifier remains structural and path/ref oriented.
- Token counts use approximate `chars / 4`; no exact tokenizer exists.
- No provider billing, reasoning-token, cached-token, or live API usage accounting exists.
- No automatic policy/prompt optimizer exists.
- Q17 Router Profile remains deferred.
- Q18 cache/local-state boundary remains deferred.
- Gateway, providers, Runtime, Service, Commander, UI, Mobile, MCP/A2A, and host implementation remain deferred.
- Generated manifest drift and raw queue-status nuance remain visible existing warnings where still applicable.

## Test Gaps

- Controller tests use deterministic fixtures and temp repos.
- No network, provider, model, LLM-as-judge, or external benchmark behavior is tested or implemented.
