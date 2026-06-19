# Diagnostic Quality Review

Duplicate-normalized diagnostics include the required information:

- affected collection, for example `declared_changed_paths`;
- first original value, for example `src//file.py`;
- second original value, for example `src/file.py`;
- shared canonical path, for example `src/file.py`.

Drive-prefix diagnostics identify the offending raw value and state that a
Windows drive prefix is not permitted for repository-relative paths.

Diagnostics are deterministic string outputs from the validator and do not
include unrelated source content or secrets.
