# Accepted File And Managed-Section Contracts

## File Entry

The accepted file-entry contract includes:

- `entry_ref`
- `target_relative_path`
- `ownership_class`
- `owner_ref`
- `source_distribution_ref`
- `source_component_ref`
- `installed_content_digest`
- `observed_target_digest`
- `portable_role`
- `mutable_by_distribution`
- `preserve_policy`
- `operation_constraints`
- `platform_notes`
- `case_sensitivity_notes`
- `first_observed_at`
- `last_verified_at`
- `evidence_refs`
- `prior_entry_ref`
- `superseded_by_ref`
- `extensions`

## Managed Section

The accepted managed-section contract includes:

- `entry_ref`
- `containing_file_path`
- `section_identity`
- `marker_format`
- `start_marker_digest`
- `end_marker_digest`
- `section_content_digest`
- `surrounding_content_preservation_policy`
- `owner_ref`
- `source_distribution_ref`
- `source_component_ref`
- `preimage_requirements`
- `update_constraints`
- `evidence_refs`
- `prior_entry_ref`
- `superseded_by_ref`
- `extensions`

Managed sections require exact section identity, exact markers, non-overlap,
duplicate-marker refusal, and manual-outside-only preservation.
