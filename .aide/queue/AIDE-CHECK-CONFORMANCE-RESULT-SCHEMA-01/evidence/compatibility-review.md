# Compatibility Review

Status:

```text
PASS_WITH_FINDING
```

The result uses:

- `schema_version: aide.conformance-result.v0`
- `protocol_version: 0.1.0`
- feature flag `minimal_conformance_result_schema`
- required predecessor `minimal_conformance_profile`

Compatibility remains limited to schema/helper/projection/validation surfaces.

The profile digest mismatch must be repaired before this result slice should be
accepted as a reliable compatibility surface.
