# Extension Review

Optional extension behavior is acceptable at the current implementation level:

- Top-level, metadata, spec, taxonomy, record, and status objects expose explicit
  `extensions` maps.
- Unknown optional features are tolerated with warnings.
- Unknown required features and `requires.*` extension keys fail closed.

No material extension finding is opened by this check.
