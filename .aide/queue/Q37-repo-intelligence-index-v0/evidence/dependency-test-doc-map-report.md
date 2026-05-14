# Q37 Dependency, Test, And Doc Map Report

## Dependency Map

- output: `.aide/repo/dependency-map.json`
- records: 1,543
- import references: 599
- local path references: 5,641
- unresolved references: 16,004

The dependency scanner looks for Python imports, local path strings, config
references, and deterministic repo-local references. It does not execute code.

## Test Map

- output: `.aide/repo/test-map.json`
- records: 35

The test map uses test file names, test paths, and obvious module/path
references to identify likely targets. Confidence is conservative and does not
prove coverage quality.

## Doc Link Map

- output: `.aide/repo/doc-link-map.json`
- doc records: 1,015
- stale doc-link candidates: 9,335

The doc map captures Markdown links and deterministic inline path references.
The stale count is intentionally broad because Q37 errs toward inspection
candidates instead of silence.

## Generated And Orphan Maps

- generated-map records: 835
- orphan candidates: 451

Generated and orphan outputs use candidate language only. Q37 does not call
anything dead, safe to remove, or safe to move.
