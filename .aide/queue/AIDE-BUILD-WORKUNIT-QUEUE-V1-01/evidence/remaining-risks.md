# Remaining Risks

- YAML parsing is a conservative stdlib subset suitable for current AIDE queue task shapes, not a general YAML implementation.
- JSON Schema validation remains a minimal local subset, not full Draft 2020-12 validation.
- WorkUnit queue projections are not yet accepted until an independent check and acceptance task run.
- `PyYAML` is unavailable in the current environment; this is non-blocking because the slice does not depend on it.
