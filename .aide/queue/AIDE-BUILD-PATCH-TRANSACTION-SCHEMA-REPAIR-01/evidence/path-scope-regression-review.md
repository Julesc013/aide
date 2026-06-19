# Path-Scope Regression Review

Focused repaired cases:

- `C:repo/file.txt` now fails because drive-prefixed paths are not valid
  repository-relative PatchTransaction locators.
- `C:repo\file.txt`, `C:/repo/file.txt`, `C:\repo\file.txt`, and
  `z:relative.txt` also fail portably.
- `src//file.py` plus `src/file.py` now fails because both declarations
  normalize to `src/file.py`.
- duplicate-normalized entries now fail in `allowed_paths`, `forbidden_paths`,
  and `declared_changed_paths`.
- duplicate diagnostics include both original path strings and the shared
  canonical path.

Preserved cases:

- POSIX absolute paths still fail.
- Windows absolute paths still fail.
- UNC-style absolute paths still fail.
- Traversal paths still fail.
- Empty or dot-only paths still fail.
- Declared paths outside allowed scope still fail.
- Forbidden path matches still fail.
- Direct allowed/forbidden overlap still fails.
- A single separator-normalized path remains valid.
- Prefix-boundary checks still fail closed.
- Valid distinct normalized paths remain accepted.

The repair is intentionally local to scope validation.
