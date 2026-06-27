# Validation

Overall result: `PASS_WITH_WARNINGS`

Material findings: `0`

Missing evidence: `0`

Validation summary:

- Focused UpdatePlan compile and tests passed.
- UpdatePlan `status`, `project`, and `validate` passed with warnings and zero errors.
- DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord predecessor regressions passed with warnings and zero blocking errors.
- Q43-Q48 no-apply/no-publish validators passed.
- Broad AIDE validation passed.
- Source build task inspect/evidence passed with `missing_evidence: 0`.
- Check-local semantic probe passed.
- Report/evidence local path, secret-like, and source-output misuse scans passed.
- Git whitespace validation passed.

Warnings are accepted as non-material:

- UpdatePlan v1 remains proposed until acceptance.
- Same-session independence is reduced.
- Standalone PyYAML is unavailable, with AIDE-native YAML validation covering task files.
- Live projected unknown and never-touch conflicts are fail-closed warning-class conflicts.
