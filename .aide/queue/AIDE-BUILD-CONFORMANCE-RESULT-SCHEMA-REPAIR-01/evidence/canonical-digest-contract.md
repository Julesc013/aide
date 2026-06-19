# Canonical Digest Contract

Algorithm:

```text
sha256-canonical-json-v1
```

Definition:

```python
json.dumps(
    profile,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
).encode("utf-8")
```

Digest source:

```text
.aide/reports/conformance-profile/profiles.json
```

The digest is independent of pretty-printing, newline style, indentation,
dictionary insertion order, operating system, and local absolute paths.
