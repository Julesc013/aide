# Safe importer write-boundary baseline

- Source: remote-observed `dev@5dfa75e632b09f732a8150376db6840bcf149ed3`.
- In the current importer, `portable_target_path` validates ancestors before
  `apply_import_operation` later calls `atomic_write_bytes_if_changed` with a
  pathname. A writable ancestor can change between those operations.
- The independent owned-file repair review found the analogous parent-junction
  race in repair candidate `49f38d12`; this task covers the remaining importer
  write path. The corrected repair helper is still under test and rereview.
- No adversarial importer test or native effect is claimed by this baseline.
