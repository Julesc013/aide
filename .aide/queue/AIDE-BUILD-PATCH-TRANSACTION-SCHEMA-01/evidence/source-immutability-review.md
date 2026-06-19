# Source Immutability Review

The helper hashes source inputs before and after projection.

Current validation reports:

```text
source_artifacts_mutated: false
deterministic_projection: true
```

The source set includes the schema/helper/CLI/ReferenceID/envelope files and the
operational-health/ConformanceResult predecessor reports needed for this slice.

The generated `sample-unified.diff` is a report artifact, not an applied target
file.
