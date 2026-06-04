# Validator Summary

`AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` adds the report-only AIDE Lite command group:

- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`

The validator uses stdlib JSON parsing and structural checks. It does not require `jsonschema`, does not materialize fixture target files, and does not execute lifecycle apply.

## Validated Boundaries

- lifecycle schemas declare required fields, `schema_version` constants, and `needs_review` gates;
- examples are marked as examples and include required fields;
- report/dry-run examples keep mutation flags false;
- explicit target paths reject absolute paths, traversal, and protected path targets;
- example operation types stay in `update_managed_section`, `report`, `validate`, and `noop`;
- rollback-compatible examples keep `rollback_execution_implemented: false`;
- capability labels do not claim production-ready or release-ready status.
