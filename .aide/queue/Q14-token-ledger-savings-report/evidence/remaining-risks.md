# Q14 Remaining Risks

## Remaining Risks

- Token counts are approximate `chars / 4` estimates, not exact tokenizer output.
- Q14 does not integrate provider billing, real API usage, reasoning-token accounting, or cached-token accounting.
- Token savings do not prove quality preservation; Q15 Golden Tasks v0 must add deterministic quality scaffolding.
- Regression warnings are simple path-to-previous-record comparisons and do not understand semantic value.
- Budget matching is surface-based and may return `unknown_budget` for new or uncommon surfaces.
- The context compiler remains heuristic until later symbol/import/test graph phases.
- The verifier remains structural and path-based until later semantic checks.
- `.aide.generated` manifest drift and older raw queue-status nuance remain visible existing warnings.
- `.aide/scripts/tests` direct discovery passes, but `python -m unittest discover -s .aide/scripts/tests -t .` remains a known hidden-directory import limitation.
- No local state/cache boundary exists until Q18.
- No Gateway, router, provider integration, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, automatic GPT review, LLM-as-judge behavior, automatic repair, or autonomous loop was implemented.
