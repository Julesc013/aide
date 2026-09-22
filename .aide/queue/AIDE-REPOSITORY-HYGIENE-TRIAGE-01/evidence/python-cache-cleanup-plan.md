# Python Cache Cleanup Plan

## Candidate

- Cache directories: 20.
- Cached files: 69.
- Cached bytes: 1,351,417.
- Tracked files: 0.
- Non-ignored files: 0.

Exact directories:

- `.aide/scripts/__pycache__`
- `.aide/scripts/tests/__pycache__`
- `core/apply/__pycache__`
- `core/compat/__pycache__`
- `core/compat/tests/__pycache__`
- `core/gateway/__pycache__`
- `core/gateway/tests/__pycache__`
- `core/harness/__pycache__`
- `core/harness/tests/__pycache__`
- `core/protocol/__pycache__`
- `core/providers/__pycache__`
- `core/providers/tests/__pycache__`
- `scripts/__pycache__`
- `shared/__pycache__`
- `shared/cli/__pycache__`
- `shared/config/__pycache__`
- `shared/core/__pycache__`
- `shared/diagnostics/__pycache__`
- `shared/protocol/__pycache__`
- `shared/tests/__pycache__`

The apply must verify exact path-set equality, repository containment,
non-reparse directories and descendants, ignored status, and zero tracked files
before recursively deleting only these generated Python bytecode directories.

Ignored task evidence is excluded from this candidate. Git reports zero object
store garbage, so no Git object prune or garbage collection is proposed.
