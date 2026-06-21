# Fixture Replay Review

```json
{
  "failed_count": 5,
  "fixture_count": 32,
  "passed_count": 27,
  "results": [
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "path.absolute"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/absolute_path_escape.json",
      "invalid_digest_ok": true,
      "name": "absolute_path_escape",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot",
        "digest.source",
        "path.absolute",
        "selected_files.exact_set"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "diagnostic.registry"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/arbitrary_diagnostic_severity.json",
      "invalid_digest_ok": true,
      "name": "arbitrary_diagnostic_severity",
      "observed_error_codes": [
        "diagnostic.registry",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "reference.closure"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/broken_evidence_ref.json",
      "invalid_digest_ok": true,
      "name": "broken_evidence_ref",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "reference.closure"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "ownership.semantic"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/conflicting_ownership.json",
      "invalid_digest_ok": true,
      "name": "conflicting_ownership",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "ownership.semantic"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "reference.closure"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/dangling_artifact_reference.json",
      "invalid_digest_ok": true,
      "name": "dangling_artifact_reference",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "reference.closure"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "digest.source"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/digest_mismatch.json",
      "invalid_digest_ok": true,
      "name": "digest_mismatch",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot",
        "digest.source"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "event.sequence"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/duplicate_event_sequence.json",
      "invalid_digest_ok": true,
      "name": "duplicate_event_sequence",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.sequence"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "identity.duplicate"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/duplicate_identity.json",
      "invalid_digest_ok": true,
      "name": "duplicate_identity",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "identity.duplicate"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "event.correlation"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/event_correlation_mismatch.json",
      "invalid_digest_ok": true,
      "name": "event_correlation_mismatch",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.correlation"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "authority.canonical_overclaim"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/generated_projection_marked_canonical.json",
      "invalid_digest_ok": true,
      "name": "generated_projection_marked_canonical",
      "observed_error_codes": [
        "authority.canonical_overclaim",
        "digest.bundle_self"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "diagnostic.registry"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/invalid_diagnostic_severity.json",
      "invalid_digest_ok": true,
      "name": "invalid_diagnostic_severity",
      "observed_error_codes": [
        "diagnostic.registry",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "reference.syntax"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/invalid_reference_id.json",
      "invalid_digest_ok": true,
      "name": "invalid_reference_id",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.correlation"
      ],
      "operation_count": 1,
      "result": "FAILED_VALIDATION"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "refusal.registry"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/invalid_refusal_mapping.json",
      "invalid_digest_ok": true,
      "name": "invalid_refusal_mapping",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "refusal.registry"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "refusal.registry"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/invented_refusal.json",
      "invalid_digest_ok": true,
      "name": "invented_refusal",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "refusal.registry"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "spec.required"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/missing_host_id.json",
      "invalid_digest_ok": true,
      "name": "missing_host_id",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "spec.required"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "selected_files.exact_set"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/missing_required_contract.json",
      "invalid_digest_ok": true,
      "name": "missing_required_contract",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot",
        "digest.source",
        "selected_files.exact_set"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "revision.binding"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/mixed_record_revision.json",
      "invalid_digest_ok": true,
      "name": "mixed_record_revision",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "revision.binding"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "capability.mutation"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/mutation_capability_claim.json",
      "invalid_digest_ok": true,
      "name": "mutation_capability_claim",
      "observed_error_codes": [
        "capability.implemented_set",
        "capability.mutation",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "capability.mutation"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/mutation_capability_labeled_readonly.json",
      "invalid_digest_ok": true,
      "name": "mutation_capability_labeled_readonly",
      "observed_error_codes": [
        "capability.implemented_set",
        "capability.mutation",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "event.sequence"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/non_deterministic_ordering.json",
      "invalid_digest_ok": true,
      "name": "non_deterministic_ordering",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.sequence"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "path.traversal"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/path_traversal.json",
      "invalid_digest_ok": true,
      "name": "path_traversal",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot",
        "digest.source",
        "path.traversal",
        "selected_files.exact_set"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "command.invocation"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/private_tool_bypass_declaration.json",
      "invalid_digest_ok": true,
      "name": "private_tool_bypass_declaration",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "FAILED_VALIDATION"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "status.false_boundary"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/provider_network_worker_claim.json",
      "invalid_digest_ok": true,
      "name": "provider_network_worker_claim",
      "observed_error_codes": [
        "digest.bundle_self",
        "status.false_boundary"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "cardinality.singleton"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/second_host_capability_set.json",
      "invalid_digest_ok": true,
      "name": "second_host_capability_set",
      "observed_error_codes": [
        "capability.forbidden_set",
        "capability.implemented_set",
        "cardinality.singleton",
        "digest.bundle_self",
        "digest.projection_index",
        "identity.duplicate",
        "record_count"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "digest.snapshot"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/snapshot_digest_not_validated.json",
      "invalid_digest_ok": true,
      "name": "snapshot_digest_not_validated",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "revision.binding"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/stale_revision.json",
      "invalid_digest_ok": true,
      "name": "stale_revision",
      "observed_error_codes": [
        "digest.bundle_self",
        "revision.binding"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "compat.required_capability"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/unknown_required_capability.json",
      "invalid_digest_ok": true,
      "name": "unknown_required_capability",
      "observed_error_codes": [
        "digest.bundle_self"
      ],
      "operation_count": 1,
      "result": "FAILED_VALIDATION"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "schema.version"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/unsupported_version.json",
      "invalid_digest_ok": true,
      "name": "unsupported_version",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "schema.version"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "workbench.authority"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/workbench_authority_overclaim.json",
      "invalid_digest_ok": true,
      "name": "workbench_authority_overclaim",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "operation_count": 1,
      "result": "FAILED_VALIDATION"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "authority.role"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/wrong_authority_role.json",
      "invalid_digest_ok": true,
      "name": "wrong_authority_role",
      "observed_error_codes": [
        "digest.bundle_self"
      ],
      "operation_count": 1,
      "result": "FAILED_VALIDATION"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "repository.identity"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/wrong_repository_identity.json",
      "invalid_digest_ok": true,
      "name": "wrong_repository_identity",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.snapshot",
        "digest.source",
        "repository.identity"
      ],
      "operation_count": 1,
      "result": "PASS"
    },
    {
      "base_digest_ok": true,
      "detail": null,
      "deterministic_replay": true,
      "expected_error_codes": [
        "ownership.semantic"
      ],
      "fixture_path": ".aide/fixtures/dominium-readonly-seam/negative/wrong_semantic_owner.json",
      "invalid_digest_ok": true,
      "name": "wrong_semantic_owner",
      "observed_error_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "ownership.semantic"
      ],
      "operation_count": 1,
      "result": "PASS"
    }
  ],
  "schema_version": "aide.dominium-readonly-seam.repair-check.negative-results.v0"
}
```
