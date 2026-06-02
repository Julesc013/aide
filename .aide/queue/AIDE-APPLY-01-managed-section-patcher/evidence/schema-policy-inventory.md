# Schema And Policy Inventory

## Policies

- `.aide/policies/managed-section-markers.yaml`: marker syntax, uniqueness, nesting, manual-content boundary, and fixture-only limits.
- `.aide/policies/managed-sections.yaml`: AIDE-APPLY-01 no-apply posture, conflict classes, rollback evidence, validation requirements, and next review gate.

## Schemas

- `.aide/apply/managed-section-operation.schema.json`: transaction-compatible managed-section operation record.
- `.aide/apply/managed-section-patch.schema.json`: planned fixture patch record.
- `.aide/apply/managed-section-conflict.schema.json`: missing, duplicate, malformed, nested, and hash-mismatch conflict record.
- `.aide/apply/managed-section-report.schema.json`: report-only status/fixture/conflict/rollback boundary record.

## Examples And Fixtures

- `.aide/examples/apply/managed-section.valid.example.json`
- `.aide/examples/apply/managed-section.missing-marker-conflict.example.json`
- `.aide/examples/apply/managed-section.duplicate-marker-conflict.example.json`
- `.aide/examples/apply/managed-section-patch.example.json`
- `.aide/examples/apply/managed-section-report.example.json`
- `.aide/examples/apply/managed-section-fixtures/{valid_input.md,replacement.md,expected_output.md,missing_marker.md,duplicate_marker.md}`

## Validation Coverage

- `managed-section validate`: PASS, 333 checks.
- `managed_section_schema_presence_golden`: PASS.
- `managed_section_marker_policy_golden`: PASS.
