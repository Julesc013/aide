# Example Events Review

## Result

PASS_WITH_WARNINGS

## Findings

- Example events JSON parses.
- Example event count is 4.
- Example events are deterministic projections.
- Example events are projection-only.
- Example events report `recorded: false`.
- Each example includes `event_ref`, valid `event_type`, subject refs, and report/evidence refs where present.
- Causation and correlation refs validate where present.
- Actor refs are structurally valid and use `aide://source/...` in projected examples.

## Accepted Boundary

Example events are accepted only as projection records. They are not runtime event emissions, are not appended to a store, and do not reconstruct or replay system state.
