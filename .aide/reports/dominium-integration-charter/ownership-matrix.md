# Ownership Matrix

| Owner | Owns | Must Not Own |
| --- | --- | --- |
| AIDE | WorkUnit, WorkerRun, TestJob, generic ReferenceID, EvidencePacket, EventRecord, CapabilityManifest, ConformanceProfile, ConformanceResult, AdapterManifest, ContextPack, current PatchTransaction proposal, future DevelopmentTransaction envelope, generic host/bridge contracts | Dominium product law, command meaning, document/scene semantics, Domino process execution, Workbench operator truth |
| Dominium | product law, domain semantics, command/result/refusal/diagnostic meaning, validation meaning, documents, scenes, graph, assets, packages, product policy, Workbench product behavior | generic AIDE protocol authority, AIDE queue authority, generic WorkerRun/TestJob lifecycle |
| Domino | deterministic execution capabilities, process execution, storage/order/execution mechanics, replay, apply/undo operations, hot-path execution | AIDE queue truth, Workbench presentation, product-facing meaning unless delegated |
| Workbench | native context capture, selection/workspace projection, preview presentation, approval interaction, apply requests, view/action models, evidence inspection, operator interaction | product truth, private tool bypass, scheduler authority, provider credentials, silent mutation, AIDE protocol authority |

Shared concepts must be owned directly, referenced by stable ID, projected read-only, translated through a versioned bridge, composed through an envelope, or explicitly not mapped.
