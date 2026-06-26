# File Entry Review

Independent source inspection and a check-local probe found that file records
use compact fields such as `record_id`, `target_path`, `source_ref`, and
`content_digest`.

Required fields from the check oracle are absent from emitted records and the
schema, including:

- `entry_ref`
- `target_relative_path`
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
- `prior_entry_ref`
- `superseded_by_ref`

Disposition: material finding `ownership.file_entry_contract_incomplete`.
