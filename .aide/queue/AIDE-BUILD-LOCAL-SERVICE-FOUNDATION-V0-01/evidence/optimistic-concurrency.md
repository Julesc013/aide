# Optimistic Concurrency

- objects carry monotonically increasing integer versions
- stale expected versions fail closed with `resource_version_conflict`
- object creation accepts expected version `0` or no expected version
- update with matching current version increments the version

No distributed locks or leases are implemented.
