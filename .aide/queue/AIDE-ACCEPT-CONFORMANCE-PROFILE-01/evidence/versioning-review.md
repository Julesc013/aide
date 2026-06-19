# Versioning Review

Result: `PASS`

Accepted versioning facts:

- profile_version: `1.0.0`
- profile_ref: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- profile ref binds to the exact version
- future ConformanceResult records must bind to this exact profile version
- case ordering and profile ordering are deterministic
- paths are repository-relative
- no absolute local path is part of the profile contract

This acceptance does not implement a schema migration engine.
