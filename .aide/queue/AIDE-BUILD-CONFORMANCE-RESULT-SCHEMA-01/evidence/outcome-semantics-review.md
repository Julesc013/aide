# Outcome Semantics Review

Observed case outcomes are limited to:

```text
PASS
PASS_WITH_WARNINGS
FAIL
ERROR
SKIPPED
UNAVAILABLE
NOT_RUN
```

Aggregate outcomes are limited to:

```text
PASS
PASS_WITH_WARNINGS
FAIL
ERROR
INCOMPLETE
```

The helper treats missing required cases, required `NOT_RUN`, required
`SKIPPED`, required `UNAVAILABLE`, failed required cases, errored required
cases, duplicate case results, and unknown case results as closed or invalid
states.

A valid result record can represent non-passing outcomes; validity is not the
same as satisfaction or admission.
