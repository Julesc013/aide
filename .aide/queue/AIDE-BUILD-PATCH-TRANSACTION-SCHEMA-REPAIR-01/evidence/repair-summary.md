# Repair Summary

Changed implementation:

- `core/protocol/patch_transaction.py`
  - added `_has_windows_drive_prefix`;
  - rejects drive-prefixed strings before accepting repository-relative paths;
  - added `_append_unique_normalized`;
  - rejects duplicate-normalized allowed, forbidden, and declared paths;
  - duplicate diagnostics identify both original entries and the shared
    canonical path.

Changed tests:

- `.aide/scripts/tests/test_aide_patch_transaction.py`
  - added `test_drive_prefixed_relative_paths_fail`;
  - added drive-prefix variant coverage;
  - added duplicate-normalized coverage for `allowed_paths`,
    `forbidden_paths`, and `declared_changed_paths`;
  - added diagnostic coverage for colliding original values and canonical path.

The repair keeps PatchTransaction as a no-apply protocol slice. It does not
implement approval, policy evaluation, patch apply, rollback, admission, trust,
AdapterManifest, ContextPack v2, Test Broker runtime, worker execution, Service,
Commander, Workbench, provider/model/network/Gateway/GitHub behavior,
branch/worktree automation, release, promotion, or target-repository mutation.
