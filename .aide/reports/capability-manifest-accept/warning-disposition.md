# CapabilityManifest Acceptance Warning Disposition

All warnings are non-blocking for `minimal_capability_manifest`.

| Warning | Blocking | Disposition | Future task |
| --- | --- | --- | --- |
| CapabilityManifest declares capability state but does not prove conformance. | false | accepted_with_warning | AIDE-BUILD-CONFORMANCE-PROFILE-01 |
| CapabilityManifest does not admit adapters. | false | accepted_with_warning | future AdapterManifest chain |
| CapabilityManifest does not execute capabilities. | false | accepted_with_warning | future runtime/adapter tasks |
| ConformanceProfile is not implemented. | false | deferred | AIDE-BUILD-CONFORMANCE-PROFILE-01 |
| ConformanceResult is not implemented. | false | deferred | AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01 |
| PatchTransaction is not implemented. | false | deferred | AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01 |
| AdapterManifest is not implemented. | false | deferred | future AdapterManifest chain |
| ContextPack v2 is not implemented. | false | deferred | future ContextPack v2 chain |
| Latest-task-packet drift remains unresolved. | false | accepted_with_warning | future ContextPack or context refresh task |
| Accepted predecessor capabilities preserve accepted_with_warnings. | false | accepted_with_warning | none |
