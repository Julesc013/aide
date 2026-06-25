# Source Contamination Boundary

DistributionManifest validation rejects portable inclusion of:

- absolute paths;
- path traversal;
- `.aide.local/**`;
- `.env` and secret-like paths;
- source-generated `.aide/context/latest-*`;
- source-generated `.aide/reports/**`;
- source-generated latest install/repair/upgrade/rollback/uninstall outputs;
- local logs and caches.

Forbidden member fixtures fail with:

```text
distribution.forbidden_member
distribution.source_state_contamination
```

The live manifest validation reports `absolute_local_paths_suppressed: true`.
