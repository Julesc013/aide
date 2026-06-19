# AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01

Create and process `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked `AIDE-ACCEPT-CONTEXTPACK-V2-01` record if present, and preserve the
original blocked build/check records.

Review the complete ContextPack chain:

- original blocked `AIDE-BUILD-CONTEXTPACK-V2-01`
- original blocked `AIDE-CHECK-CONTEXTPACK-V2-01`
- `AIDE-RESUME-BUILD-CONTEXTPACK-V2-01`
- `AIDE-RESUME-CHECK-CONTEXTPACK-V2-01`

Accept only the minimal projection capability if all gates pass. Acceptance must
not imply model/provider calls, embeddings, worker execution, adapter admission,
trust, patch apply, target mutation, runtime, Service, Commander, Workbench,
release, or production readiness.
