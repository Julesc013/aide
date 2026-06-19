# Normalized Duplicate Repair

Status: `PASS_WITH_WARNINGS`

The validator now rejects duplicate-normalized entries in:

- `allowed_paths`
- `forbidden_paths`
- `declared_changed_paths`

The repair does not silently deduplicate. It rejects ambiguity after raw unsafe
forms are checked and repo-relative normalization has produced a canonical path.

Example diagnostic:

```text
declared_changed_paths: duplicate normalized path: src/file.py from 'src//file.py' and 'src/file.py'
```

The diagnostic preserves:

- the colliding canonical path;
- the first original input;
- the later conflicting original input.

No case-folding rule was added.
