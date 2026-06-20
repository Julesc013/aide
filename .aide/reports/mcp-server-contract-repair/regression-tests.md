# Regression Tests

Focused MCP contract tests passed:

```text
Ran 65 tests
OK
```

New regressions cover omitted no-cursor fields, null cursor failures,
non-string cursor failures, valid opaque string cursors, `-32002`
resource-not-found mapping, preserved custom refusal codes, JSON-RPC `2.0`,
request/response ID alignment, ID-free notifications, deterministic projection,
source immutability, and unsupported command rejection.
