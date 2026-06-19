# Outcome Semantics Review

Status:

```text
PASS
```

Allowed observed outcome vocabulary was preserved:

```text
PASS
PASS_WITH_WARNINGS
FAIL
ERROR
SKIPPED
UNAVAILABLE
NOT_RUN
```

The projected result uses only `PASS` and `PASS_WITH_WARNINGS`.

Every required case outcome is accepted by the corresponding profile case after
normalizing `ACCEPTED` to `PASS` and `ACCEPTED_WITH_WARNINGS` to
`PASS_WITH_WARNINGS`.
