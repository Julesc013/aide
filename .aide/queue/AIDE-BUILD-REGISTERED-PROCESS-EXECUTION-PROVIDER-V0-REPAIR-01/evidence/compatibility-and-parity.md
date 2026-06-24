# Compatibility And Parity

Focused Dominium parity tests passed after the repair:

```text
Ran 7 tests
OK
```

The Dominium adapter behavior remains bounded to the accepted command-boundary
meaning:

- exact argv preserved;
- `shell=False` preserved;
- one launcher call for a valid invocation;
- typed refusal semantics preserved;
- aggregate-validation success remains unclaimed;
- service-adapter entry remains unclaimed;
- mutation observation remains scoped to declared probe coverage.

The live Dominium command was not rerun.
