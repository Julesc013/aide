# Conflict Report

## Policy And Schema

- policy: `.aide/policies/install-conflicts.yaml`
- report schema: `.aide/install/conflict-report.schema.json`
- record schema: `.aide/install/conflict-record.schema.json`

## Latest Report

- JSON: `.aide/install/latest-conflict-report.json`
- Markdown: `.aide/install/latest-conflict-report.md`
- conflict_count: 458
- blocking_count: 0
- no_apply: true

## Conflict Types

Q43 recognizes:

- existing_manual_file
- existing_managed_file
- target_specific_file
- source_state_leak
- schema_version_mismatch
- unsupported_old_schema
- local_state_tracked
- secret_like_path
- generated_target_state_collision
- ambiguous_owner
- unsafe_overwrite

## Mandatory Migration Notes

Migration is not automatic in Q43. The install plan records mandatory migration candidates only when a mandatory reason exists, such as unsupported schema, validation blocker, unsafe old format, ambiguous truth, or source-state contamination.
