# Q15 Remaining Risks

- Golden tasks are deterministic local checks only.
- No external coding benchmark is implemented.
- No model/provider evals are implemented.
- No exact tokenizer is implemented.
- No semantic correctness validation for arbitrary code patches is implemented.
- Q16 Outcome Controller is not implemented.
- Router Profile remains deferred until Q17.
- Cache/local-state boundary remains deferred until Q18.
- Gateway, providers, Runtime, Service, Commander, UI, Mobile, MCP/A2A, and host implementation remain deferred.
- Generated manifest source-fingerprint drift and older raw queue-status nuance remain visible existing warnings.
- Python unittest discovery with `-s .aide/scripts/tests -t .` remains a documented hidden-directory limitation; direct discovery without `-t .` passes.
