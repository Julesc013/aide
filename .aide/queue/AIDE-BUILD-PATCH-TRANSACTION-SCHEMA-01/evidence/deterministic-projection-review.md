# Deterministic Projection Review

The projection writes deterministic outputs under:

```text
.aide/reports/patch-transaction/
```

The generated sample artifact is:

```text
.aide/reports/patch-transaction/sample-unified.diff
```

with digest:

```text
sha256:5747bd0d486a73c1b363b0f4c8af974b4ee1f24968a53221eba2c89f187b3c5f
```

Repeated projection comparison is part of `patch-transaction validate` and the
focused unit tests. Both confirmed deterministic output.
