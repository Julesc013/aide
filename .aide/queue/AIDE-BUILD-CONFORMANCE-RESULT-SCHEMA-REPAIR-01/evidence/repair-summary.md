# Repair Summary

Status: PASS_WITH_WARNINGS

The repair separates profile identity from validation annotation:

- `load_pristine_accepted_conformance_profile()` returns the accepted profile payload without appending warnings.
- `profile_digest()` now uses `sha256-canonical-json-v1`.
- `build_conformance_result()` computes the digest before any validation annotation can be applied.
- `validate_conformance_result()` reloads the pristine profile source and validates against that digest.

Corrected digest:

```text
sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70
```
