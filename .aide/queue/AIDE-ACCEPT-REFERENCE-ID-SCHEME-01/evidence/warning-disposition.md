# Warning Disposition

All warnings are non-blocking for `minimal_reference_id_scheme` acceptance.

| Warning | Source | Blocking | Disposition | Reason | Future Task |
| --- | --- | --- | --- | --- | --- |
| ReferenceID is syntactic/projection-only. | build, check, accept | false | accepted_with_warning | The accepted capability is identity/projection only. | AIDE-BUILD-EVENT-RECORD-SCHEMA-01 begins event records, not runtime resolution. |
| Full Draft 2020-12 JSON Schema validation remains deferred. | build, check, accept | false | deferred | Local minimal schema validation passed and matches nearby protocol slices. | Future schema hardening task if required. |
| Runtime registry/resolver service is not implemented. | build, check, accept | false | accepted_with_warning | Runtime lookup is explicitly outside ReferenceID acceptance. | Future runtime/resolver task only after queue authorization. |
| EventRecord is not implemented. | build, check, accept | false | deferred | EventRecord is the next build task after acceptance, not part of ReferenceID. | AIDE-BUILD-EVENT-RECORD-SCHEMA-01. |
| OKF knowledge bundle is not implemented. | build, check, accept | false | deferred | OKF follows EventRecord in the frozen order. | Future OKF task. |
| Reconciler is not implemented. | accept | false | deferred | Reconciler is later protocol work. | Future Reconciler task. |
| CapabilityManifest is not implemented. | accept | false | deferred | Capability declaration is later protocol work. | Future CapabilityManifest task. |
| ConformanceProfile is not implemented. | accept | false | deferred | Conformance admission is later protocol work. | Future ConformanceProfile task. |
| PatchTransaction is not implemented. | build, check, accept | false | deferred | Patch mutation is later and requires separate authorization. | Future PatchTransaction task. |
| AdapterManifest is not implemented. | build, check, accept | false | deferred | Adapters remain later than conformance and patch records. | Future AdapterManifest task. |
| ContextPack v2 is not implemented. | build, check, accept | false | deferred | ContextPack v2 is after adapter work in the frozen order. | Future ContextPack v2 task. |
| latest-task-packet.md is stale relative to queue truth. | build, check, accept | false | stale | `.aide/queue/index.yaml` is canonical; stale packet was not used as authority. | Separate hygiene task if needed. |

No warning requires hardening or repair before acceptance.
