# Drive Prefix Probes

Independent probes used a raw-path rule equivalent to `^[A-Za-z]:` before
ordinary slash normalization.

All requested variants failed production scope validation:

- `C:repo/file.txt`
- `C:repo\file.txt`
- `C:/repo/file.txt`
- `C:\repo\file.txt`
- `c:relative.txt`
- `z:folder/file.py`
- `Z:file.py`

Existing unsafe forms also failed: POSIX absolute paths, Windows absolute paths,
UNC-like paths, traversal, empty path, and dot-only path.

`docs/time:note.md` remained valid as a repo-relative path containing a colon
after the first path segment.
