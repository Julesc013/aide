# Normalized Duplicate Recheck

Duplicate-normalized path entries fail closed in every relevant collection:

- `allowed_paths`
- `forbidden_paths`
- `declared_changed_paths`

Checked duplicate forms include:

- `src//file.py` and `src/file.py`
- `src/./file.py` and `src/file.py`
- `src\file.py` and `src/file.py`
- `src///nested//file.py` and `src/nested/file.py`

The implementation does not silently deduplicate. It returns a validation error
for the affected collection and keeps the canonical collision value visible.

Distinct valid paths such as `src/file.py` and `src/other.py` remain accepted.
