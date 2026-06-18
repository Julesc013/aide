# Versioning Review

The profile uses a stable SemVer identity:

- `profile_id`: `minimal_capability_manifest`
- `profile_version`: `1.0.0`
- `profile_ref`: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`

The helper requires the `profile_ref` to match the `profile_id` and
`profile_version` pair and rejects non-SemVer versions.

Protocol helper version remains `0.1.0`, matching the existing minimal protocol
slice pattern.
