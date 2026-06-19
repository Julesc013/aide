# Determinism And Immutability Evidence

Canonical repeated projection was run twice through:

```text
py -3 .aide/scripts/aide_lite.py patch-transaction project
```

PatchTransaction report tree digest before and after:

```text
cc9bdb0cad8cf356a901d4e55cd4e69093ff35f26a4430d50e2e2a61c7a6d9e2
```

The digest did not change. Source inputs were unchanged. Canonical fixtures and
accepted predecessor reports were not modified.

Result: `PASS_WITH_WARNINGS`

Warning: a reduced temporary-copy probe was not used as acceptance evidence; it
does not replace the canonical live-repo projection check.
