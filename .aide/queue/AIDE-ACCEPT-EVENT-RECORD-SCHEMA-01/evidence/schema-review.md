# Schema Review

## Result

PASS_WITH_WARNINGS

## Accepted

- `.aide/protocol/aide-event-record.schema.json` exists and parses.
- The schema represents `kind: EventRecord`.
- The top-level shape follows `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- Compatibility metadata is present under `metadata.compatibility`.
- `event_ref` uses the `aide://event/<id>` form.
- Event type, subject ref, causation, correlation, occurred-at timestamp, local sequence, actor, payload, evidence refs, report refs, explicit non-capabilities, projection-only status, and `recorded: false` status are represented.

## Non-Claims

The schema does not claim event sourcing runtime, append-only event store, runtime event log, state reconstruction, replay, scheduler, leases, supervisor, Service, Commander, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, or broad runtime behavior.

## Warning

Full JSON Schema Draft 2020-12 validation remains deferred; the repo uses its current minimal subset validator for this slice.
