# Remaining Risks

- EventRecord is only a schema/helper/projection surface; there is no runtime event store or replay behavior.
- Full JSON Schema Draft 2020-12 validation remains deferred.
- Event family names are reserved vocabulary only; they do not implement OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, or runtime coordination.
- The live Task OS `latest_task_id` remains stale relative to accepted queue truth.
- The next task must be `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`, not OKF.
