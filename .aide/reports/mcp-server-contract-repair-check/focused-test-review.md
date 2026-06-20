# Focused Test Review

Focused MCP tests passed:

```text
Ran 65 tests
OK
```

The suite includes regressions for omitted cursor fields, omitted nextCursor
fields, valid string cursors, null and non-string rejection, resource-not-found
`-32002`, old `-32043` rejection, custom refusal preservation, deterministic
projection, source immutability, and unsupported command rejection.
