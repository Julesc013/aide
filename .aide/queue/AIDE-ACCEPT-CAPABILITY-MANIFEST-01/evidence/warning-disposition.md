# Warning Disposition

All warnings are non-blocking for `minimal_capability_manifest`.

| Warning | Source | Blocking | Disposition | Reason | Future task |
| --- | --- | --- | --- | --- | --- |
| CapabilityManifest declares capability state but does not prove conformance. | build, check, acceptance | false | accepted_with_warning | This is the intended declaration-only boundary. | AIDE-BUILD-CONFORMANCE-PROFILE-01 |
| CapabilityManifest does not admit adapters. | build, check, acceptance | false | accepted_with_warning | Adapter admission requires later conformance and adapter contracts. | future AdapterManifest chain |
| CapabilityManifest does not execute capabilities. | build, check, acceptance | false | accepted_with_warning | Runtime and execution remain deferred. | future runtime/adapter tasks |
| ConformanceProfile is not implemented. | build, check, acceptance | false | deferred | It is the next Track A build slice after this acceptance. | AIDE-BUILD-CONFORMANCE-PROFILE-01 |
| ConformanceResult is not implemented. | build, check, acceptance | false | deferred | It depends on ConformanceProfile acceptance. | AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01 |
| PatchTransaction is not implemented. | build, check, acceptance | false | deferred | Mutation safety follows admission primitives. | AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01 |
| AdapterManifest is not implemented. | build, check, acceptance | false | deferred | Adapter declarations come after mutation/admission foundations. | future AdapterManifest chain |
| ContextPack v2 is not implemented. | build, check, acceptance | false | deferred | ContextPack v2 follows adapter and interop ordering. | future ContextPack v2 chain |
| Latest-task-packet drift remains unresolved. | build, check, acceptance | false | accepted_with_warning | Queue truth remains canonical and context refresh is not authorized here. | future ContextPack or context refresh task |
| Accepted predecessor capabilities preserve accepted_with_warnings. | build, check, acceptance | false | accepted_with_warning | Warning preservation is required and must not be flattened to done. | none |
