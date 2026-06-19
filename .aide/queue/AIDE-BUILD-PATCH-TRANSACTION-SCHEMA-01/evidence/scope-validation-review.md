# Scope Validation Review

The helper validates explicit mutation scope:

- repo-relative path normalization;
- rejection of absolute paths;
- rejection of `..` traversal;
- rejection of empty normalized paths;
- declared paths must be inside allowed scope;
- declared paths must not match forbidden scope;
- direct allowed/forbidden overlap fails closed.

Focused tests cover absolute paths, traversal, outside-allowed paths, forbidden
matches, and ambiguous direct overlap.

The deterministic example declares only:

```text
fixtures/patch-transaction/synthetic-example.txt
```

with allowed scope:

```text
fixtures/patch-transaction/**
```

No target file was created or mutated.
