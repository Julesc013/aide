# Accepted Boundary

Accepted capability:

```text
project_lock_v0
```

Accepted meaning:

- A ProjectLock v0 object can select one accepted DistributionManifest by
  distribution digest and manifest payload digest.
- It can record selected required and optional components by digest.
- It can record selected artifact refs and dependency closure.
- It treats release channel as informational rather than identity-authoritative.
- It preserves explicit extension maps and tolerates unknown optional features.
- It rejects unknown required features, required unknown extensions, unaccepted
  manifests, digest drift, component graph defects, dependency defects,
  invalid overlay/source-state/path/secret references, and unsupported protocol
  ranges.

The accepted capability remains a selection and binding object only.
