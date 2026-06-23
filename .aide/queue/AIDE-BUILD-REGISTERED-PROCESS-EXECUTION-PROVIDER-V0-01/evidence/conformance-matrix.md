# Conformance Matrix

| Area | Coverage |
| --- | --- |
| Preflight | wrong workspace identity, missing executable, digest mismatch, invalid spec, Dominium revision mismatch, Dominium dirty workspace |
| Invocation | exact argv, `shell=False`, controlled cwd, sanitized environment, one launcher call, timeout, bounded stream summaries, deterministic receipt digests |
| Decoding | typed result, typed refusal, nonzero typed refusal, nonzero without domain result, empty output, malformed output, decoder exception |
| State | unchanged state, tracked mutation, partial coverage, probe failure, Dominium mutation refusal |
| Evidence | stream scrubbing, stable receipt correlation, no domain names in generic provider |
| Parity | Dominium adapter preserves the accepted semantic refusal and capability boundary |

Warnings remain for v0 non-capabilities listed in
`explicit-non-capabilities.md`.
