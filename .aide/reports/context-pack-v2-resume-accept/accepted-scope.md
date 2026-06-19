# Accepted Scope

Accepted:

- deterministic ContextPack v2 projection
- source/report references by repo-relative path and sha256
- required sections and reference-kind validation
- explicit no-execution status facts
- AIDE Lite `context-pack-v2 status/project/validate`
- report generation and inspection

Not accepted:

- model/provider/network calls
- embedding generation
- worker or command execution
- adapter admission or trust
- patch application
- target repository mutation
- runtime/service behavior
