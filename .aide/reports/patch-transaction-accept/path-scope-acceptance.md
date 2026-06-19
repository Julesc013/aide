# Path Scope Acceptance

Status: `BLOCKED`

Scope safety is not accepted.

The independent check found:

```text
path_scope_drive_prefixed_relative_accepted
path_scope_duplicate_normalization_accepted
```

The live check evidence says the production validator accepted:

```text
allowed_paths: ["C:repo/**"]
declared_changed_paths: ["C:repo/file.txt"]
```

and:

```text
allowed_paths: ["src/**"]
declared_changed_paths: ["src//file.py", "src/file.py"]
```

PatchTransaction acceptance must wait for repair and independent repair check.
