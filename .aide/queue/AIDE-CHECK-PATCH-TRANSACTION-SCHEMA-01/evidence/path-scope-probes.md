# Path Scope Probe Evidence

Result: `FAILED_VALIDATION`

Independent adversarial probes found two material fail-closed defects.

## Material Failures

1. Drive-prefixed relative path accepted.

```text
allowed_paths: ["C:repo/**"]
declared_changed_paths: ["C:repo/file.txt"]
production_result: scope_valid true
expected: invalid
```

2. Duplicate-normalized declarations accepted.

```text
allowed_paths: ["src/**"]
declared_changed_paths: ["src//file.py", "src/file.py"]
production_result: scope_valid true
expected: invalid
```

## Passing Negative Cases

The validator failed closed for:

- POSIX absolute paths;
- Windows absolute paths;
- UNC paths;
- traversal paths;
- empty and dot-only paths;
- declared paths outside allowed scope;
- declared paths matching forbidden scope;
- direct allowed/forbidden overlap;
- prefix-boundary errors such as treating `src-old/` as inside `src/`.

Separator normalization for `src\\file.py` under `src/**` was valid.
