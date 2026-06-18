# ConformanceCase Index

- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- case_count: 10
- result_generated: false
- admission_performed: false

- capability-manifest-schema-parses (required, evaluator=schema_parse)
- capability-manifest-projection-json-valid (required, evaluator=json_report_valid)
- capability-manifest-validation-pass-with-warnings (required, evaluator=predecessor_validator)
- capability-manifest-acceptance-evidence-complete (required, evaluator=queue_task_status)
- capability-manifest-declaration-only-boundary (required, evaluator=boundary_review)
- accepted-warning-debt-classified (required, evaluator=report_review)
- reference-and-event-refs-parse (required, evaluator=reference_id_validator)
- source-artifacts-not-mutated-by-profile (required, evaluator=source_mutation_sentinel)
- latest-task-packet-drift-classified (advisory, evaluator=report_review)
- track-b-b1-barrier-authorized-track-a (optional, evaluator=report_review)
