# Prompt Summary

The user requested broad project performance and reliability hardening. AIDE policy classifies that kind of broad request as unsafe to execute directly, so this QFIX narrows the work to an evidence-backed hot path:

- AIDE Lite `test` / `selftest` runtime;
- full golden-task validation remains available through `eval run`;
- no provider/model/network calls;
- no target repo mutation;
- no speculative rewrites.
