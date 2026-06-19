# PatchTransaction Path-Scope Repair

Status: `PASS_WITH_WARNINGS`

## Repaired Findings

- `path_scope_drive_prefixed_relative_accepted`: `C:repo/file.txt` style paths
  now fail validation because repository-relative PatchTransaction paths cannot
  carry a Windows drive prefix. The checked variants include `C:repo/file.txt`,
  `C:repo\file.txt`, `C:/repo/file.txt`, `C:\repo\file.txt`, and
  `z:relative.txt`.
- `path_scope_duplicate_normalization_accepted`: declarations such as
  `src//file.py` and `src/file.py` now fail validation as duplicate normalized
  paths. Duplicate-normalized entries also fail in `allowed_paths` and
  `forbidden_paths`.
- Duplicate diagnostics preserve both original path strings and the shared
  canonical path, for example `src//file.py`, `src/file.py`, and `src/file.py`.

## Preserved Behavior

- A single separator-normalized path such as `src\\file.py` remains valid under
  `src/**`.
- Valid distinct normalized paths such as `src/file.py` and `src/other.py`
  remain accepted.
- Prefix-boundary checks remain fail-closed; `src-old/file.py` is not inside
  `src/**`.
- No apply, approval, policy, admission, trust, rollback, runtime, or
  target-repository mutation behavior was added.
