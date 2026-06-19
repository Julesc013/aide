# AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01

Create and process `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked ContextPack records. Review the original blocked build/check records,
the resume build, and this resume check.

Accept only the minimal ContextPack v2 projection capability if all gates pass.
Acceptance must not imply model/provider calls, embeddings, worker execution,
adapter admission, trust, patch apply, target mutation, runtime, Service,
Commander, Workbench, release, promotion, or production readiness.
