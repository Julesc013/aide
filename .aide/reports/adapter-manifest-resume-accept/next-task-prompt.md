# AIDE-RESUME-BUILD-CONTEXTPACK-V2-01

Create and process `AIDE-RESUME-BUILD-CONTEXTPACK-V2-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked `AIDE-BUILD-CONTEXTPACK-V2-01` record as historical evidence; do not
rewrite or reuse it.

Build a deterministic, evidence-bound ContextPack v2 schema/projection slice
only after confirming `AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01` accepted
`minimal_adapter_manifest_schema` with complete evidence.

The ContextPack v2 slice should compile bounded context from accepted queue,
protocol, evidence, OKF, Reconciler, capability, conformance, and explicit
non-capability surfaces. It must not execute workers, call providers, mutate
repositories, apply patches, admit adapters, grant trust, or implement runtime
behavior.
