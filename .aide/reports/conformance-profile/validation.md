# ConformanceProfile Validation Report

- status: PASS_WITH_WARNINGS
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- recommended_next_task: AIDE-CHECK-CONFORMANCE-PROFILE-01

## Checks

- schema_exists: true
- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- helper_exists: true
- cli_registered: true
- reports_generated: true
- profiles_json_valid: true
- profile_index_json_valid: true
- case_index_json_valid: true
- case_ids_unique: true
- dependencies_resolve: true
- dependency_cycles_absent: true
- requirement_levels_valid: true
- known_required_evaluators: true
- unknown_required_evaluator_fails_closed: true
- unknown_optional_evaluator_warns: true
- unknown_advisory_evaluator_warns: true
- required_cases_have_accepted_outcomes: true
- required_cases_fail_closed: true
- profile_lifecycle_candidate: true
- evidence_requirements_declared: true
- source_evidence_exists: true
- profile_boundary_valid: true
- result_not_generated: true
- execution_not_implemented: true
- admission_not_performed: true
- trusted_not_promoted: true
- explicit_non_capabilities_preserved: true
- predecessor_compatibility_preserved: true
- overclaiming_check_passed: true
- forbidden_ops_preserved: true

## Validation Errors

- none

## Warnings

- ConformanceProfile defines required checks but does not execute them.
- ConformanceResult is not implemented by this slice.
- Admission policy and acceptance decisions remain separate future work.
- The profile lifecycle is candidate and must be checked independently before acceptance.
- Unknown required evaluators fail closed; optional and advisory unknown evaluators warn only.
- Accepted predecessor warning debt is preserved rather than repaired.
- Stale generated latest-task-packet drift remains reported; queue truth is canonical.
