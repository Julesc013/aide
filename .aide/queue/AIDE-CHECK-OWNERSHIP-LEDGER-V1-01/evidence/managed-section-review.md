# Managed Section Review

The implementation has a `vendor_managed_section` class plus compact
`section_id` and `managed_section_identity` fields.

Required managed-section fields from the check oracle are absent from the
schema/helper output:

- `containing_file_path`
- `section_identity`
- `marker_format`
- `start_marker_digest`
- `end_marker_digest`
- `section_content_digest`
- `surrounding_content_preservation_policy`
- `preimage_requirements`
- `update_constraints`

There is no committed fixture coverage for duplicate markers, overlapping
sections, nested sections, marker identity mismatch, manual outside text
preservation, or section/file ownership conflict.

Disposition: material finding `ownership.managed_section_contract_incomplete`.
