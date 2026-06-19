# Normalized Duplicate Probes

Duplicate-normalized inputs were independently normalized and then checked
against production validation.

Every duplicate pair failed in:

- `allowed_paths`;
- `forbidden_paths`;
- `declared_changed_paths`.

Checked pairs:

- `src//file.py` and `src/file.py`;
- `src/./file.py` and `src/file.py`;
- `src\file.py` and `src/file.py`;
- `src///nested//file.py` and `src/nested/file.py`.

The validator did not silently deduplicate.
