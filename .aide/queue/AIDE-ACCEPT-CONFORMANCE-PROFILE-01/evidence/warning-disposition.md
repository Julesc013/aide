# Warning Disposition

All warnings are non-blocking.

| Warning | Blocking | Disposition | Follow-up |
| --- | --- | --- | --- |
| ConformanceProfile defines checks but does not execute them. | false | accepted_with_warning | `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` |
| ConformanceResult is not implemented. | false | deferred | `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01` |
| No conformance runner or case execution exists. | false | deferred | Future bounded conformance-runner task |
| Conformance admission is not implemented. | false | deferred | Future policy/admission task |
| ConformanceCase is modeled inline rather than in a separate `$defs` block. | false | accepted_with_warning | Future versioned/backward-compatible extraction only |
| `.aide/context/latest-task-packet.md` is stale relative to queue truth. | false | deferred | Future authorized context refresh |
| PatchTransaction, AdapterManifest, ContextPack v2, adapters, runtime, providers, target apply, release, and promotion remain deferred. | false | future_work | Future queue tasks |

Warnings are truthful, visible, and do not expand the accepted capability.
