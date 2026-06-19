# Drive Prefix Recheck

The repaired validator rejects all requested drive-prefixed path variants:

- `C:repo/file.txt`
- `C:repo\file.txt`
- `C:/repo/file.txt`
- `C:\repo\file.txt`
- `c:relative.txt`
- `z:folder/file.py`
- `Z:file.py`

The independent expectation used a bounded raw-path rule equivalent to
`^[A-Za-z]:` before ordinary slash normalization. Production validation matched
that expectation and returned failed scope reports with `drive prefix`
diagnostics.

Existing fail-closed behavior also remains intact for POSIX absolute paths,
Windows absolute paths, UNC-like paths, traversal, empty paths, and dot-only
paths.

A repo-relative path containing a colon after the first path segment,
`docs/time:note.md`, remains accepted by both independent normalization and the
production validator. This preserves the narrower drive-prefix rule without
inventing a broader colon policy.
