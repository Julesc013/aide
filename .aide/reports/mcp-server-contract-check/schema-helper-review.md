# Schema And Helper Review

The schema parses and the generated contract preserves the established envelope
shape:

```text
apiVersion
kind
metadata
spec
status
```

The build helper and CLI report `PASS_WITH_WARNINGS`. The independent check
does not accept that output as sufficient proof. It found fixture-level pinned
MCP issues that the build validator did not catch.

Material impact: helper validation coverage is insufficient for the two failed
fixture classes, but no implementation was repaired in this check.
