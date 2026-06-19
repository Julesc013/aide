# ConformanceResult Validation Report

- status: PASS_WITH_WARNINGS
- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- recommended_next_task: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

## Checks

- schema_exists: true
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- helper_exists: true
- cli_registered: true
- reports_generated: true
- results_json_valid: true
- result_index_json_valid: true
- case_result_index_json_valid: true
- projection_json_valid: true
- case_ids_unique: true
- case_results_bind_to_profile: true
- observed_outcomes_valid: true
- case_results_execution_false: true
- case_results_runner_null: true
- observation_mode_evidence_projection: true
- observation_execution_false: true
- observation_runner_null: true
- profile_digest_matches: true
- required_cases_accounted: true
- record_complete: true
- profile_requirements_satisfied: true
- record_valid_independent: true
- admission_not_performed: true
- subject_not_admitted: true
- trusted_not_promoted: true
- result_boundary_valid: true
- explicit_non_capabilities_preserved: true
- predecessor_compatibility_preserved: true
- overclaiming_check_passed: true
- forbidden_ops_preserved: true

## Validation Errors

- none

## Warnings

- case retained warning debt: capability-manifest-validation-pass-with-warnings
- case retained warning debt: capability-manifest-acceptance-evidence-complete
- case retained warning debt: capability-manifest-declaration-only-boundary
- case retained warning debt: accepted-warning-debt-classified
- case retained warning debt: reference-and-event-refs-parse
- case retained warning debt: latest-task-packet-drift-classified
- Profile requirements satisfied does not admit or trust the subject.
