# Validator Hardening

Validator injection check passed:

```text
validator_injection_check PASS cases=33 note=diagnostics include fixture and field; invalid type inferred from injected case
```

The validator rejects temporary reintroduction of:

- explicit null cursor;
- explicit null nextCursor;
- numeric, boolean, object, and array cursor values;
- numeric, boolean, object, and array nextCursor values;
- resource-not-found error code `-32043`.

The validator returns to `PASS_WITH_WARNINGS` for correct fixtures. Remaining
warnings are no-runtime/no-full-schema warnings.
