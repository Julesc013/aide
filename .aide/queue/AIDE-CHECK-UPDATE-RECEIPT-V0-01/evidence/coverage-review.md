# Coverage Review

Schema/helper support:

- Supported operation receipt classes: 23
- Operation receipt classes observed in fixtures: 21
- Supported skipped-operation reasons: 18
- Skipped-operation reasons observed in fixtures: 8

Missing positive fixture rows:

- Operation classes: `manual_review_recorded`, `operation_failed`
- Skipped reasons: `case_collision`, `missing_approval`, `missing_rollback_requirement`, `policy_refusal`, `postimage_mismatch`, `preimage_mismatch`, `symlink_or_reparse_uncertainty`, `unknown_required_feature`, `unsupported_operation`, `validation_failed`

Disposition:

- Warning-class. The schema and helper enumerate the missing values and the validator rejects unknown classes or reasons. Required positive and negative fixture names are present on disk. The gap is fixture granularity rather than a missing semantic validator.

No material finding was opened.
