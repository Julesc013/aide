# ReferenceID And EventRecord Review

The Reconciler checks ReferenceID and EventRecord report presence and parses their JSON status fields.

Current result:

- ReferenceID reports loaded.
- EventRecord reports loaded.
- No current `reference_mismatch` finding was emitted.
- No current `event_mismatch` finding was emitted.

ReferenceID and EventRecord reports remain projection-only predecessors. The Reconciler does not rewrite references or events.
