# Independent Probe Summary

Check-local probes confirmed additional fail-closed cases beyond the named invalid fixture list:

- missing `target_project_ref` -> `rollback_bundle.target_project_missing`
- missing `candidate_project_lock_ref` -> `rollback_bundle.candidate_project_lock_missing`
- missing `prior_install_record_refs` -> `rollback_bundle.install_record_missing`
- candidate distribution mismatch -> `rollback_bundle.candidate_distribution_mismatch`
- source distribution mismatch -> `rollback_bundle.source_distribution_mismatch`
- reverse project overlay mutation -> `rollback_bundle.project_overlay_reverse_mutation`
- reverse runtime generated mutation -> `rollback_bundle.runtime_generated_reverse_mutation`
- reverse evidence only mutation -> `rollback_bundle.evidence_only_reverse_mutation`
- install apply authority claim -> `rollback_bundle.apply_authority_claimed`
- update apply authority claim -> `rollback_bundle.apply_authority_claimed`
- uninstall apply authority claim -> `rollback_bundle.apply_authority_claimed`

All check-local probes returned `FAILED_VALIDATION` with the expected refusal code.

Schema/projection field inspection confirmed the required metadata and spec fields are present in both the schema and generated projection.

Reverse-operation representation:

- Schema enum includes all required reverse operation classes.
- Fixture corpus validates `remove_added_managed_file`, `remove_added_managed_section`, and `rollback_unavailable`.
- Live projection includes only classes reachable from the current accepted UpdatePlan source operations.
