# Example Events Review

## Result

PASS_WITH_WARNINGS

## Findings

- `.aide/reports/event-record/example-events.json` parses as JSON.
- Example event count is 4.
- All example events validate with the helper.
- All example event refs parse through ReferenceID syntax.
- All projected examples have `status.recorded: false`.
- All projected examples have `status.projection_only: true`.
- Example event refs use the `aide://event/EVT-...` pattern.

## Warnings

Example events are report projections only. They are not appended to a runtime event log and cannot be replayed as system state.
