# Remaining Risks

- Full JSON Schema Draft 2020-12 validation remains deferred.
- ReferenceID does not resolve references at runtime.
- EventRecord, OKF, PatchTransaction, adapter manifests, conformance/capability records, ContextPack v2, and runtime coordination remain future work.
- The check is not an acceptance; acceptance belongs to `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`.
- `.aide/context/latest-task-packet.md` remains stale relative to live queue truth.

Mitigation:

- Preserve these as explicit non-capabilities.
- Route the next step to acceptance review, not EventRecord implementation.
