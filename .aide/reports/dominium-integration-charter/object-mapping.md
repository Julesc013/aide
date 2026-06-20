# Object Mapping

| AIDE object | Dominium/Workbench relation | Semantic owner | Mapping |
| --- | --- | --- | --- |
| WorkUnit | command/validation intent container | AIDE | references Dominium command intent; does not own command meaning |
| WorkerRun | external attempt record | AIDE | records attempt metadata only |
| TestJob | validation execution attempt | AIDE | wraps Dominium validation intent and evidence refs |
| ContextPack | bounded context projection | AIDE | fed by ContextDescriptor and stable source refs |
| EvidencePacket | proof reference aggregation | AIDE | aggregates native evidence without rewriting meaning |
| EventRecord | audit/correlation event | AIDE | correlates native events without universal event-store claim |
| CapabilityManifest | generic declaration | AIDE | compares to Dominium capability registry; grants nothing |
| ConformanceProfile | admission test requirements | AIDE | declares requirements; does not activate providers |
| ConformanceResult | observed generic result | AIDE | records observed results; grants no use by itself |
| AdapterManifest | external integration declaration | AIDE | declares bridge/adapter; grants no trust or execution |
| PatchTransaction | current file-oriented proposal | AIDE | remains no-apply and non-domain |
| future DevelopmentTransaction | domain-neutral governance envelope | AIDE | composes policy/preview/approval refs around domain payload |
| Blocker/repair/resume | queue recovery mapping | AIDE | maps typed refusals into bounded queue recovery |

Forbidden transformations include copying Dominium command semantics into AIDE WorkUnit, rewriting native evidence semantics, using AdapterManifest as admission, extending PatchTransaction into domain mutation, and treating Workbench projection as product truth.
