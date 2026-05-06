# Q10 Remaining Risks

- Q10 awaits independent review; status is `needs_review`, not `passed`.
- Q09 also remains `needs_review`, so Harness doctor still recommends Q09 review even though Q10 proceeded by explicit prompt authorization.
- Token counts are approximate `chars / 4`; exact tokenizer support is deferred.
- Provider billing integration and formal token ledger recording are deferred to later ledger work.
- Context compiler behavior remains shallow until Q11; Q10 uses snapshot metadata and context refs only.
- Verifier/evidence-gate behavior remains limited until Q12.
- Evidence-review workflow remains manual until Q13.
- Token ledger and savings regression tracking remain deferred until Q14.
- Golden task quality proof remains deferred until Q15.
- Router, cache boundary, Gateway, provider adapters, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app behavior, and autonomous loops remain unimplemented by design.
- Python unittest discovery with `-s .aide/scripts/tests -t .` fails because the hidden `.aide` start directory is not importable as a top-level package; direct discovery with `-s .aide/scripts/tests` passes and is documented.
- Raw queue-status nuance for Q00-Q03, Q05, and Q06 remains visible rather than normalized.
