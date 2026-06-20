# Material Findings

- `identity.lookalike_rejected`: Lookalike repository identity must fail before source inspection
- `digest.bundle_self_recompute`: Bundle self digest must be calculated after final validation_summary/status fields
- `diagnostics.truncation_disclosure`: Diagnostic projection truncation is not explicitly recorded in omission summary
- `refusals.truncation_disclosure`: Refusal projection truncation is not explicitly recorded in omission summary
- `schema.effectiveness`: Public schema meaningfully constrains v0 seam documents
- `fixtures.negative_replayability`: Negative fixtures are independently replayable without importing production mutators
- `conformance.independence`: Each conformance expectation has distinct assertion evidence
- `demo.elapsed_time`: Demo elapsed time is hard-coded or unmeasured as zero
- `negative.mixed_record_revision`: Valid-but-wrong record source revision is accepted
- `negative.snapshot_digest_not_validated`: Snapshot digest fields can be corrupted without validation failure
- `negative.second_host_capability_set`: Second singleton HostCapabilitySet is accepted
- `negative.dangling_artifact_reference`: Dangling artifact reference is accepted after digest refresh
- `negative.wrong_semantic_owner`: Valid-but-wrong semantic owner is accepted
- `negative.mutation_capability_labeled_readonly`: Forbidden mutation capability is accepted when labeled read_only
- `negative.duplicate_event_sequence`: Duplicate event sequence is accepted because only sorting is checked
- `negative.arbitrary_diagnostic_severity`: Arbitrary diagnostic severity is accepted when severity_valid remains true
- `negative.invented_refusal`: Invented refusal projection is accepted
- `negative.missing_host_id`: HostManifest required field removal is accepted
