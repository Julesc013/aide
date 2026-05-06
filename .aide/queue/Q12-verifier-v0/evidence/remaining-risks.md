# Q12 Remaining Risks

## Deferred By Design

- No LLM-as-judge behavior.
- No automatic code repair.
- No semantic diff analysis.
- No exact tokenizer.
- No provider billing integration or formal token ledger.
- No golden-task quality proof.
- No Gateway, router, cache, provider adapter, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loop.

## Known Technical Limits

- The verifier is structural and path-based; it does not understand code semantics.
- Diff-scope checks classify paths only and do not inspect patch intent.
- File-reference extraction is conservative and focuses on backticks or markdown links.
- Secret scanning is heuristic; it catches obvious key-like values but cannot prove absence of sensitive material.
- Token counts still use `ceil(chars / 4)`.
- Evidence-packet validation checks sections and some signs of recorded commands; it does not validate test logs semantically.

## Carried Forward

- `.aide/generated/manifest.yaml` source fingerprint drift remains visible in Harness validation and was not refreshed by Q12.
- Q09, Q10, Q11, and Q12 remain at review gates until independent review records outcomes.
- `.aide/profile.yaml` may still lag the newest queue focus; Q12 keeps `.aide/queue/` as the live queue-state source.
