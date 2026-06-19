# Path Scope Review

Status: `FAILED_VALIDATION`

Independent path-scope probes found two material fail-closed defects.

## Material Findings

### path_scope_drive_prefixed_relative_accepted

Expected: drive-prefixed relative paths fail where repository-relative paths are
required.

Observed: the production validator returned `scope_valid: true` for:

```text
allowed_paths: ["C:repo/**"]
declared_changed_paths: ["C:repo/file.txt"]
```

Impact: a PatchTransaction can treat an ambiguous Windows drive-relative path as
valid mutation scope.

### path_scope_duplicate_normalization_accepted

Expected: duplicate-normalized declarations fail as ambiguous.

Observed: the production validator returned `scope_valid: true` for:

```text
allowed_paths: ["src/**"]
declared_changed_paths: ["src//file.py", "src/file.py"]
```

Impact: a PatchTransaction can contain two declared path strings that normalize
to the same locator without an ambiguity error.

## Passing Scope Cases

The validator failed closed for POSIX absolute paths, Windows absolute paths,
UNC-style paths, traversal, dot-only paths, declared paths outside allowed
scope, forbidden matches, direct allowed/forbidden overlap, and prefix-boundary
errors such as treating `src-old/` as inside `src/`.

Separator normalization for `src\\file.py` under `src/**` behaved as expected.
