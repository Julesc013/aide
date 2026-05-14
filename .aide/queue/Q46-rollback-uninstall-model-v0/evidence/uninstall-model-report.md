# Uninstall Model Report

## Policy Surface

- `.aide/policies/uninstall.yaml`
- `.aide/policies/uninstall-classes.yaml`
- `.aide/policies/uninstall-safety.yaml`
- `.aide/policies/uninstall-verification.yaml`

The uninstall policy defines deterministic local observation, owned-file and
preserved-file classification, no-apply planning, dry-run, review, and future
verification. It explicitly states that uninstall is not blanket `.aide`
deletion.

## Schema Surface

- `.aide/uninstall/uninstall-observation.schema.json`
- `.aide/uninstall/uninstall-plan.schema.json`
- `.aide/uninstall/uninstall-operation.schema.json`
- `.aide/uninstall/uninstall-dry-run.schema.json`
- `.aide/uninstall/uninstall-verification.schema.json`
- `.aide/uninstall/uninstall-report.schema.json`

Each uninstall operation carries `apply_allowed: false`,
`delete_allowed: false`, and `managed_section_removal_allowed: false` by
default.

## Generated Artifacts

- `.aide/uninstall/latest-uninstall-observation.json`
- `.aide/uninstall/latest-uninstall-observation.md`
- `.aide/uninstall/latest-uninstall-plan.json`
- `.aide/uninstall/latest-uninstall-plan.md`
- `.aide/uninstall/latest-uninstall-dry-run.json`
- `.aide/uninstall/latest-uninstall-dry-run.md`
- `.aide/uninstall/latest-uninstall-verification-plan.md`

Latest uninstall plan summary: 1790 operations, 1557 preserved paths, 233
future removal candidates, 672 unknown-ownership records, 0 blockers, and
`no_apply: true`.

## Command Surface

- `uninstall observe`
- `uninstall plan`
- `uninstall dry-run`
- `uninstall validate`
- `uninstall status`
- `uninstall explain PATH_OR_ISSUE`
- `uninstall classes`

All commands are advisory. They write only `.aide/uninstall/latest-*` outputs
and do not delete, overwrite, remove managed sections, or apply uninstall.
