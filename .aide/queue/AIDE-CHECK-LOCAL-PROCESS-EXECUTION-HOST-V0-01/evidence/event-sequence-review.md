# Event Sequence Review

- REQUEST_CHANGES: build records one synthesized `RunObserved` event with sequence `1`.
- REQUEST_CHANGES: raw fixture events are not retained as a stream.
- REQUEST_CHANGES: malformed and non-monotonic event stream failure paths are not proven.
