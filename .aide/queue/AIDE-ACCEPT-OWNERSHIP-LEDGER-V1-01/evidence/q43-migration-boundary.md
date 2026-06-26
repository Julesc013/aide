# Q43 Migration Boundary

Accepted behavior:

- Q43 migration is deterministic projection evidence only.
- Known Q43 classes map to exact v1 ownership classes.
- `unknown` maps to `unknown` with manual review required.
- Unmapped classes fail closed with `ownership.migration_unmapped`.
- Migration records preserve source class, target class, disposition, manual
  review state, reason/evidence posture, and no-apply boundary.

Accepted Q43 mappings:

- `managed_aide_file` -> `vendor_managed_file`
- `managed_aide_section` -> `vendor_managed_section`
- `target_project_file` -> `project_owned`
- `target_overlay` -> `project_overlay`
- `target_generated` -> `project_generated`
- `runtime_generated` -> `runtime_generated`
- `local_only` -> `local_only`
- `evidence_record` -> `evidence_only`
- `preserved_legacy` -> `preserved_legacy`
- `never_touch` -> `never_touch`
- `unknown` -> `unknown` with manual review

This acceptance does not authorize migration apply or target repository
mutation.
