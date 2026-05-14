# Rollback Model Report

## Policy Surface

- `.aide/policies/rollback.yaml`
- `.aide/policies/rollback-classes.yaml`
- `.aide/policies/rollback-safety.yaml`
- `.aide/policies/rollback-verification.yaml`

The rollback policy defines deterministic local observation, ownership/plan
inspection, classification, no-apply planning, dry-run, review, and future
verification. Q46 forbids rollback apply mode, target mutation, file overwrite,
file deletion, and managed-section removal.

## Schema Surface

- `.aide/rollback/rollback-observation.schema.json`
- `.aide/rollback/rollback-plan.schema.json`
- `.aide/rollback/rollback-operation.schema.json`
- `.aide/rollback/rollback-dry-run.schema.json`
- `.aide/rollback/rollback-verification.schema.json`
- `.aide/rollback/rollback-report.schema.json`

Each rollback operation carries `apply_allowed: false`,
`overwrite_allowed: false`, `delete_allowed: false`, and
`managed_section_removal_allowed: false` by default.

## Generated Artifacts

- `.aide/rollback/latest-rollback-observation.json`
- `.aide/rollback/latest-rollback-observation.md`
- `.aide/rollback/latest-rollback-plan.json`
- `.aide/rollback/latest-rollback-plan.md`
- `.aide/rollback/latest-rollback-dry-run.json`
- `.aide/rollback/latest-rollback-dry-run.md`
- `.aide/rollback/latest-rollback-verification-plan.md`

Latest rollback plan summary: 229 operations, 885 preserved paths, 0 blockers,
and `no_apply: true`.

## Command Surface

- `rollback observe`
- `rollback plan`
- `rollback dry-run`
- `rollback validate`
- `rollback status`
- `rollback explain PATH_OR_ISSUE`
- `rollback classes`

All commands are advisory. They write only `.aide/rollback/latest-*` outputs and
do not restore, overwrite, delete, or remove managed sections.
