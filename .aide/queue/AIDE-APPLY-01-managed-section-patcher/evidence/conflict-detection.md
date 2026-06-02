# Conflict Detection

## Conflict Classes Covered

- `missing_marker`
- `duplicate_marker`
- `malformed_marker`
- `marker_order_invalid`
- `nested_marker`
- `section_name_mismatch`
- `existing_hash_mismatch`
- `binary_or_unreadable`

## Evidence

- `core/apply/tests/test_managed_sections.py`: PASS, covers missing, duplicate, nested, malformed, ordering, and hash mismatch paths.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS, 138 checks.
- `.aide/reports/managed-section-conflict-report.md` is written from missing-marker and duplicate-marker fixtures.
- `managed_section_conflict_detection_golden`: PASS.

## Behavior

Conflicts produce report records. They do not trigger active repo mutation or automatic repair.
