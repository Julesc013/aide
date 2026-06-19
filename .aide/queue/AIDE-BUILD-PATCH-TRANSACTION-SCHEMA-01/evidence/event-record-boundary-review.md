# EventRecord Boundary Review

PatchTransaction supports:

- `source_event_refs`
- `status_event_refs`

The deterministic example leaves both arrays empty because no live event store,
event append, replay, scheduler, lease, supervisor, runtime, or Service exists.

No EventRecord implementation or event-store behavior was changed.
