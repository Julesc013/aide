# Minimal CapabilityManifest ConformanceResult

- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- profile_digest: sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
- subject_ref: aide://capability/minimal_capability_manifest
- observation_mode: evidence_projection
- execution_performed: false
- runner_ref: None
- aggregate_outcome: PASS_WITH_WARNINGS
- record_valid: true
- record_complete: true
- profile_requirements_satisfied: true
- admission_performed: false
- subject_admitted: false
- trusted: false

## Case Results

### capability-manifest-schema-parses

- requirement_level: required
- evaluator: schema_parse
- outcome: PASS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 0

### capability-manifest-projection-json-valid

- requirement_level: required
- evaluator: json_report_valid
- outcome: PASS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 0

### capability-manifest-validation-pass-with-warnings

- requirement_level: required
- evaluator: predecessor_validator
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### capability-manifest-acceptance-evidence-complete

- requirement_level: required
- evaluator: queue_task_status
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### capability-manifest-declaration-only-boundary

- requirement_level: required
- evaluator: boundary_review
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### accepted-warning-debt-classified

- requirement_level: required
- evaluator: report_review
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### reference-and-event-refs-parse

- requirement_level: required
- evaluator: reference_id_validator
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### source-artifacts-not-mutated-by-profile

- requirement_level: required
- evaluator: source_mutation_sentinel
- outcome: PASS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 0

### latest-task-packet-drift-classified

- requirement_level: advisory
- evaluator: report_review
- outcome: PASS_WITH_WARNINGS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 1

### track-b-b1-barrier-authorized-track-a

- requirement_level: optional
- evaluator: report_review
- outcome: PASS
- observed: true
- execution_performed: false
- runner_ref: None
- warnings_count: 0
