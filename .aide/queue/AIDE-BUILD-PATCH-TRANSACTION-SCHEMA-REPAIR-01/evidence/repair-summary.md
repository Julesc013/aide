# Repair Summary

Changed implementation:

- `core/protocol/patch_transaction.py`
  - added `_has_windows_drive_prefix`;
  - rejects drive-prefixed strings before accepting repository-relative paths;
  - added `_append_unique_normalized`;
  - rejects duplicate-normalized allowed, forbidden, and declared paths.

Changed tests:

- `.aide/scripts/tests/test_aide_patch_transaction.py`
  - added `test_drive_prefixed_relative_paths_fail`;
  - added `test_duplicate_normalized_declared_paths_fail`.

The repair keeps PatchTransaction as a no-apply protocol slice. It does not
implement approval, policy evaluation, patch apply, rollback, admission, trust,
AdapterManifest, ContextPack v2, Test Broker runtime, worker execution, Service,
Commander, Workbench, provider/model/network/Gateway/GitHub behavior,
branch/worktree automation, release, promotion, or target-repository mutation.
