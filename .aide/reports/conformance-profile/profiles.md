# Minimal CapabilityManifest ConformanceProfile

- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- profile_id: minimal_capability_manifest
- profile_version: 1.0.0
- lifecycle: candidate
- subject_ref: aide://capability/minimal_capability_manifest
- profile_only: true
- result_generated: false
- admission_performed: false

## Cases

### capability-manifest-schema-parses

- title: CapabilityManifest Schema Parses
- requirement_level: required
- evaluator: schema_parse
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: none
- result_ref: None
- execution_implemented: false

### capability-manifest-projection-json-valid

- title: CapabilityManifest Projection JSON Valid
- requirement_level: required
- evaluator: json_report_valid
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: capability-manifest-schema-parses
- result_ref: None
- execution_implemented: false

### capability-manifest-validation-pass-with-warnings

- title: CapabilityManifest Validation Preserved
- requirement_level: required
- evaluator: predecessor_validator
- accepted_outcomes: PASS, PASS_WITH_WARNINGS, ACCEPTED_WITH_WARNINGS
- dependencies: capability-manifest-projection-json-valid
- result_ref: None
- execution_implemented: false

### capability-manifest-acceptance-evidence-complete

- title: CapabilityManifest Acceptance Evidence Complete
- requirement_level: required
- evaluator: queue_task_status
- accepted_outcomes: ACCEPTED, ACCEPTED_WITH_WARNINGS, PASS_WITH_WARNINGS
- dependencies: capability-manifest-validation-pass-with-warnings
- result_ref: None
- execution_implemented: false

### capability-manifest-declaration-only-boundary

- title: Declaration-Only Boundary Preserved
- requirement_level: required
- evaluator: boundary_review
- accepted_outcomes: PASS, PASS_WITH_WARNINGS, ACCEPTED_WITH_WARNINGS
- dependencies: capability-manifest-acceptance-evidence-complete
- result_ref: None
- execution_implemented: false

### accepted-warning-debt-classified

- title: Accepted Warning Debt Classified
- requirement_level: required
- evaluator: report_review
- accepted_outcomes: PASS, PASS_WITH_WARNINGS, ACCEPTED_WITH_WARNINGS
- dependencies: capability-manifest-acceptance-evidence-complete
- result_ref: None
- execution_implemented: false

### reference-and-event-refs-parse

- title: Reference And Event Refs Parse
- requirement_level: required
- evaluator: reference_id_validator
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: capability-manifest-projection-json-valid
- result_ref: None
- execution_implemented: false

### source-artifacts-not-mutated-by-profile

- title: Profile Projection Does Not Mutate Source Artifacts
- requirement_level: required
- evaluator: source_mutation_sentinel
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: capability-manifest-projection-json-valid, capability-manifest-declaration-only-boundary
- result_ref: None
- execution_implemented: false

### latest-task-packet-drift-classified

- title: Latest Task Packet Drift Classified
- requirement_level: advisory
- evaluator: report_review
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: none
- result_ref: None
- execution_implemented: false

### track-b-b1-barrier-authorized-track-a

- title: Track B B1 Barrier Authorized Track A
- requirement_level: optional
- evaluator: report_review
- accepted_outcomes: PASS, PASS_WITH_WARNINGS
- dependencies: none
- result_ref: None
- execution_implemented: false
