# Windows importer write design note

This is a read-only technical design from `/root/safe_import_write_design`,
2026-09-25. It is not source review, implementation, or acceptance evidence.
The branch has three reproduced failing oracles: managed-payload parent swap,
import-intent parent swap, and new/update racing-leaf overwrite.

For a new leaf, pin all ancestors, reject reparse points, stage and flush the
complete bytes inside the pinned parent, and publish with a handle-relative
no-replace operation. A competing leaf must remain intact. New intent and
receipt leaves require the same treatment; every directory created on the
way needs a pinned, verified parent.

For an existing managed leaf, a pathname digest followed by `os.replace`
cannot provide effect-time ownership. Open the exact leaf with read and delete
access while denying rival write/delete sharing, reject reparse points,
verify regular single-link identity and preimage through that handle, then
stage new bytes. A proposed recoverable update would persist a backup identity
in the intent, rename the verified old handle to a unique no-replace backup,
and publish the staged file no-replace. A rival leaf arriving in the gap must
be preserved, with the backup and intent retained for recovery. This has a
visible missing-leaf interval and must not be described as atomic replacement.
Existing receipt transitions and exact intent cleanup also need identity-bound
handling. Interrupted states before backup rename, in the gap, after publish,
and before receipt transition each need distinct tests and recovery behavior.

The design inference follows the published Windows API boundaries:
[ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)
and replacement rename take names without an expected target identity;
[FILE_RENAME_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_rename_info)
supports `ReplaceIfExists=FALSE` and a directory handle;
[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
defines sharing constraints; and
[FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
can bind a handle's file identity. This analysis does not prove those APIs are
implemented correctly in AIDE.

Next source action: integrate the independently accepted repair helper first,
then implement and test all importer effect paths against these invariants.
The existing path-based importer remains unsafe on this task branch.
