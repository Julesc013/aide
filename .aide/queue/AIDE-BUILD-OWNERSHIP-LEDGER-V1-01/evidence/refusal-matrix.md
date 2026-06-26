# Refusal Matrix

Validation rejects:

- ProjectLock digest mismatch.
- Missing or unknown taxonomy class.
- Duplicate record IDs.
- Unknown record classes.
- Vendor-managed files without content digest.
- Vendor-managed sections without managed-section identity.
- Unknown or never-touch records that allow apply.
- Any record enabling apply, overwrite, or delete.
- Absolute paths.
- Traversal paths.
- Source latest paths.
- Unknown required features.
- Required unknown extensions.
