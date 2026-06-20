# Validator Hardening

`validate_fixtures()` now validates the repaired subset:

- supported paginated requests allow omitted params, empty params, or string
  `params.cursor`;
- supported paginated requests reject explicit `cursor: null`;
- supported paginated requests reject numeric, object, or array cursor values;
- supported paginated results reject explicit `nextCursor: null`;
- supported paginated results reject non-string present `nextCursor` values;
- resource-not-found requires error code `-32002`;
- custom AIDE refusal fixtures retain their own codes and reason codes.

This is not a full official MCP schema validator.
