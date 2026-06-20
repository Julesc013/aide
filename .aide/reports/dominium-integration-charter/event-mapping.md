# Event Mapping

Event owners:

- AIDE owns generic `EventRecord` identity and schema.
- Dominium owns command events and domain event meaning.
- Domino owns process/replay events and replay semantics.
- Workbench owns operator interaction events and host presentation events.

Correlation rules:

- causation uses stable object refs rather than file paths;
- correlation may join WorkUnit, ContextPack, command, result/refusal, evidence, and Workbench interaction refs;
- sequence belongs to the producing event owner;
- timestamp semantics remain owner-defined until a future event-store contract exists;
- replay semantics are Domino-owned;
- resumption semantics are AIDE queue-owned when a WorkUnit or task resumes.

This charter does not claim one universal event store.
