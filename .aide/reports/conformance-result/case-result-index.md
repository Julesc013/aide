# ConformanceCaseResult Index

- status: PASS_WITH_WARNINGS
- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- case_result_count: 10
- admission_performed: false
- subject_admitted: false
- trusted: false

- capability-manifest-schema-parses (required, outcome=PASS, execution_performed=false)
- capability-manifest-projection-json-valid (required, outcome=PASS, execution_performed=false)
- capability-manifest-validation-pass-with-warnings (required, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- capability-manifest-acceptance-evidence-complete (required, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- capability-manifest-declaration-only-boundary (required, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- accepted-warning-debt-classified (required, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- reference-and-event-refs-parse (required, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- source-artifacts-not-mutated-by-profile (required, outcome=PASS, execution_performed=false)
- latest-task-packet-drift-classified (advisory, outcome=PASS_WITH_WARNINGS, execution_performed=false)
- track-b-b1-barrier-authorized-track-a (optional, outcome=PASS, execution_performed=false)
