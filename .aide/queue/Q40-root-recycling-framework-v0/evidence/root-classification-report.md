# Root Classification Report

## File Fate Summary

The generated file classification contains 1,751 file records:

- `keep`: 1,374
- `unknown`: 377

No record uses a delete fate, and every file classification has
`apply_allowed: false`.

## Review Summary

- review-required file classifications: 1,695
- root classifications: 22
- mixed root candidates: `.aide`, `core`, `shared`
- drop candidate approval: false

## Risk Heuristics Exercised

Q40 classifies roots and files with deterministic hints:

- identity-sensitive hints for profile, pack, bundle, manifest, schema,
  contract, release, and similar authority names.
- build-sensitive hints for source files, headers, project files, and build
  scripts.
- authority-sensitive hints for governance, policy, security, safety, release,
  repository, and contract surfaces.
- generated-sensitive hints for generated outputs and generated/source mixes.

## Caveats

- `unknown` fate means inspect before any future recycling map.
- `drop_candidate` is defined by policy but is never deletion approval.
- Q40 does not create move maps, salvage maps, path aliases, shims, archives, or
  rewritten references.
