# AIDE-RESUME-CHECK-CONTEXTPACK-V2-01

Create and process `AIDE-RESUME-CHECK-CONTEXTPACK-V2-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked `AIDE-CHECK-CONTEXTPACK-V2-01` record as historical evidence.

Independently check the resume ContextPack v2 build for schema/helper alignment,
source hash integrity, deterministic projection, source immutability, evidence
linkage, OKF/Reconciler/capability/conformance source references, explicit
non-capabilities, no model/provider/network calls, no embeddings, no execution,
no adapter admission, no trust, no patch apply, no target mutation, complete
reports, and complete task evidence.

If the check passes, recommend `AIDE-RESUME-ACCEPT-CONTEXTPACK-V2-01`. If a
material defect exists, recommend one bounded repair task instead. Do not accept
ContextPack v2 or begin the acceptance task from the check task.
