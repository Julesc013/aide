# Recommended Next Task

Exactly one serialized next task is recommended:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01
```

Boundary:

- build schema/projection/validation only;
- do not build an apply engine;
- do not mutate a target repository;
- preserve current warning debt and explicit non-capabilities.
