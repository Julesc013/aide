# Validator Regression Probes

The repair-check evidence records temporary in-memory invalid-fixture probes.

Accepted results:

- Explicit `cursor: null` fails validation.
- Explicit `nextCursor: null` fails validation.
- Number, boolean, object, and array cursor values fail validation.
- Number, boolean, object, and array nextCursor values fail validation.
- Resource-not-found code `-32043` fails validation.
- Valid opaque string cursor values pass.

No checked-in MCP fixtures were modified by these probes.
