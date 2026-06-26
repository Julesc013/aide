# Nine Finding Check Matrix

```json
{
  "assertions": [
    {
      "category": "extension_boundary",
      "description": "Schema has explicit extensions maps.",
      "evidence_refs": [
        "extension-boundary-review.md"
      ],
      "expected": "at least metadata/spec/status/protocol/component/artifact extension surfaces",
      "id": "extension.schema_surfaces_present",
      "observed": {
        "extension_property_count": 14
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "schema.optional_extension_boundary_missing"
    },
    {
      "category": "extension_boundary",
      "description": "Unknown optional extension maps survive finalize and validation.",
      "evidence_refs": [
        "extension-boundary-review.md"
      ],
      "expected": "valid manifest with preserved extension values",
      "id": "extension.optional_round_trip",
      "observed": {
        "codes": [],
        "preserved": true,
        "valid": true
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "schema.optional_extension_boundary_missing"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.unknown_required_feature",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.unknown_required_feature",
      "id": "extension.unknown_required_feature_refuses",
      "observed": {
        "codes": [
          "distribution.unknown_required_feature"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "schema.optional_extension_boundary_missing"
    },
    {
      "category": "digest",
      "description": "Independent canonical payload digest matches manifest status.",
      "evidence_refs": [
        "digest-recomputation.md"
      ],
      "expected": "sha256:7975e74342c5e01b28b6ad4c5a9e8f512417cd838619a855ff53702bdc8137f2",
      "id": "digest.independent_payload_matches",
      "observed": "sha256:7975e74342c5e01b28b6ad4c5a9e8f512417cd838619a855ff53702bdc8137f2",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "digest",
      "description": "Independent distribution digest matches manifest status.",
      "evidence_refs": [
        "digest-recomputation.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "digest.independent_distribution_matches",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "status.status must not affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "identity.status.status.does_not_change",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "status.recommended_next_task must not affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "identity.status.recommended_next_task.does_not_change",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "status.proposed_capability must not affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "identity.status.proposed_capability.does_not_change",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "status.validation_boolean must not affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "identity.status.validation_boolean.does_not_change",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "status.warning_extension must not affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "identity.status.warning_extension.does_not_change",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "metadata.distribution_ref must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.metadata.distribution_ref.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:4cc0e0c7e829a176c5d6bb51851cb1771d82410ca8c585d9d2c3b863866dd7c1"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "metadata.release_id must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.metadata.release_id.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:287f77c1815bc6dadec0b71b9ab0bc5765379f9d1ac8834c54479e0d76808d29"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "metadata.source_revision must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.metadata.source_revision.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:4cd4399cfe109fa8816c7761163ad1cdedc9b30b79ff4416f26df6b5a9367f4d"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "metadata.source_tree_digest must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.metadata.source_tree_digest.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:7c0a116c5c5f713f46cc94b59667f1a0a98f188d6e5e252bc4b8a1c2012790b3"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "artifact.digest must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.artifact.digest.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:b950035011c868b8374d292e8faf2f81dfa513c86f8dbe161e4c7ee905714f73"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "artifact.byte_count must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.artifact.byte_count.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:5e773ee4cc9674acbc370be5e621a2a3fa3ae0bc4aa25c946f39232296d0bdb4"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "component.digest must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.component.digest.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:9d78d7733a8bce2fc722bfe914bc3812c1837627995eaad0b03b9588328e258e"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "protocol.required_feature must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.protocol.required_feature.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:2802a0b92e8694a90e45d41f25a3061a2f4a5221de3ecb08b6b0bc002a719ba6"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "protocol.required_migration must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.protocol.required_migration.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:6af7d72bf90b9906878209d27e5a27515fc8e2bdd30e2d1f650cdcb22e632c4d"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "protocol.range must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.protocol.range.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:034d25b31075e0e223f5b75c35f01a0e8de8c46757d412f60814472ba570ce21"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "identity_boundary",
      "description": "artifact.included_set must affect distribution identity.",
      "evidence_refs": [
        "identity-boundary-review.md"
      ],
      "expected": "digest differs from base",
      "id": "identity.artifact.included_set.changes",
      "observed": {
        "base": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
        "changed": "sha256:a31376e9732c156ad44b0611d12dd5c7b916bc152c76a96ec7a53ed879d844e0"
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "identity.mutable_status_changes_distribution_digest"
    },
    {
      "category": "component_graph",
      "description": "Every component content digest recomputes independently.",
      "evidence_refs": [
        "component-graph-review.md"
      ],
      "expected": "all component digests match independent payload",
      "id": "component.independent_digest_recompute",
      "observed": [
        {
          "component_ref": "aide://distribution/component/aide-lite-pack-v0",
          "expected": "sha256:e334b1f111bae51513511a37f49b2b0bc028ea4d943c148eff0e04693449d2b5",
          "observed": "sha256:e334b1f111bae51513511a37f49b2b0bc028ea4d943c148eff0e04693449d2b5"
        }
      ],
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.component_digest_mismatch",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.component_digest_mismatch",
      "id": "component.wrong_digest_refuses",
      "observed": {
        "codes": [
          "distribution.component_digest_mismatch",
          "distribution.manifest_digest_mismatch"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.missing_artifact_ref",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.missing_artifact_ref",
      "id": "component.missing_artifact_ref_refuses",
      "observed": {
        "codes": [
          "distribution.component_digest_mismatch",
          "distribution.missing_artifact_ref"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.excluded_artifact_ref",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.excluded_artifact_ref",
      "id": "component.excluded_artifact_ref_refuses",
      "observed": {
        "codes": [
          "distribution.component_digest_mismatch",
          "distribution.excluded_artifact_ref"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.missing_component_dependency",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.missing_component_dependency",
      "id": "component.missing_dependency_refuses",
      "observed": {
        "codes": [
          "distribution.component_digest_mismatch",
          "distribution.missing_component_dependency"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.component_dependency_cycle",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.component_dependency_cycle",
      "id": "component.self_dependency_refuses",
      "observed": {
        "codes": [
          "distribution.component_dependency_cycle",
          "distribution.component_digest_mismatch"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.duplicate_component",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.duplicate_component",
      "id": "component.duplicate_ref_refuses",
      "observed": {
        "codes": [
          "distribution.duplicate_component",
          "distribution.duplicate_component_id"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.duplicate_component_id",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.duplicate_component_id",
      "id": "component.duplicate_id_refuses",
      "observed": {
        "codes": [
          "distribution.duplicate_component_id"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.manifest_invalid",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.manifest_invalid",
      "id": "component.required_component_omitted_refuses",
      "observed": {
        "codes": [
          "distribution.manifest_invalid"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "component_graph",
      "description": "Reordering components/artifacts does not change distribution digest.",
      "evidence_refs": [
        "component-graph-review.md"
      ],
      "expected": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "id": "component.reordered_equivalent_digest_stable",
      "observed": "sha256:29f51ed29e1fb1474fdc05cad7a0cb577d9fa5c572a753b6f1c58316d3c2b569",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "component.graph_integrity_not_validated"
    },
    {
      "category": "artifact_integrity",
      "description": "Included Q47 artifacts recompute with byte count, content digest, media type, compression type, checksums, and provenance.",
      "evidence_refs": [
        "artifact-integrity-review.md"
      ],
      "expected": "valid when artifact files are required",
      "id": "artifact.q47_files_recompute",
      "observed": {
        "codes": [],
        "valid": true
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.manifest_invalid",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.manifest_invalid",
      "id": "artifact.missing_file_refuses",
      "observed": {
        "codes": [
          "distribution.manifest_invalid",
          "distribution.missing_checksum"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.artifact_digest_mismatch",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.artifact_digest_mismatch",
      "id": "artifact.wrong_digest_refuses",
      "observed": {
        "codes": [
          "distribution.artifact_digest_mismatch",
          "distribution.checksum_digest_mismatch",
          "distribution.component_digest_mismatch"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.artifact_byte_count_mismatch",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.artifact_byte_count_mismatch",
      "id": "artifact.wrong_byte_count_refuses",
      "observed": {
        "codes": [
          "distribution.artifact_byte_count_mismatch"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.forbidden_member",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.forbidden_member",
      "id": "artifact.absolute_path_refuses",
      "observed": {
        "codes": [
          "distribution.forbidden_member",
          "distribution.missing_checksum",
          "distribution.source_state_contamination"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.forbidden_member",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.forbidden_member",
      "id": "artifact.traversal_path_refuses",
      "observed": {
        "codes": [
          "distribution.forbidden_member",
          "distribution.missing_checksum",
          "distribution.source_state_contamination"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.unsupported_source_kind",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.unsupported_source_kind",
      "id": "artifact.unsupported_source_kind_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_source_kind"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.duplicate_artifact",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.duplicate_artifact",
      "id": "artifact.duplicate_ref_refuses",
      "observed": {
        "codes": [
          "distribution.checksum_basename_collision",
          "distribution.duplicate_artifact"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "artifact_integrity",
      "description": "artifact_ref is the artifact identity; duplicate artifact_id is not treated as separate identity law in v1.",
      "evidence_refs": [
        "artifact-integrity-review.md"
      ],
      "expected": "no material duplicate artifact_id requirement unless identity law changes",
      "id": "artifact.duplicate_id_non_identity",
      "observed": "artifact_ref is checked; artifact_id is descriptive",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "artifact_integrity",
      "description": "Local directory artifact inventory recomputes.",
      "evidence_refs": [
        "artifact-integrity-review.md"
      ],
      "expected": "reported count, bytes, digest, and forbidden count match observed inventory",
      "id": "artifact.local_directory_recomputed",
      "observed": [
        {
          "artifact_ref": "aide://distribution/artifact/aide-lite-pack-v0-directory",
          "observed_byte_count": 2951837,
          "observed_count": 830,
          "observed_digest": "sha256:070caaebff339ff89004463a6aef3b9d61c0bfce082d8fc0343df8a9316eefc7",
          "observed_forbidden": 0,
          "reported_byte_count": 2951837,
          "reported_count": 830,
          "reported_digest": "sha256:070caaebff339ff89004463a6aef3b9d61c0bfce082d8fc0343df8a9316eefc7",
          "reported_forbidden": 0
        }
      ],
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "artifact.integrity_metadata_not_validated"
    },
    {
      "category": "path_safety",
      "description": "Invalid release artifact paths are rejected before stat/open/hash.",
      "evidence_refs": [
        "preaccess-path-safety.md"
      ],
      "expected": "no Path.exists, Path.stat, Path.open, or sha256_file calls for invalid records",
      "id": "path.preaccess_invalid_records_do_not_probe",
      "observed": [
        {
          "accessed": [],
          "path": "/tmp/outside/aide.zip",
          "raised": null
        },
        {
          "accessed": [],
          "path": "C:/outside/aide.zip",
          "raised": null
        },
        {
          "accessed": [],
          "path": "\\\\server\\share\\aide.zip",
          "raised": null
        },
        {
          "accessed": [],
          "path": "../outside/aide.zip",
          "raised": null
        },
        {
          "accessed": [],
          "path": ".aide.local/state.sqlite",
          "raised": null
        },
        {
          "accessed": [],
          "path": ".env",
          "raised": null
        }
      ],
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "path.preaccess_validation_order_violation"
    },
    {
      "category": "path_safety",
      "description": "Symlink/reparse escape is rejected where the platform permits a symlink probe.",
      "evidence_refs": [
        "preaccess-path-safety.md"
      ],
      "expected": "invalid or unavailable with warning",
      "id": "path.symlink_escape_rejected_where_practical",
      "observed": {
        "attempted": true,
        "reason": "distribution.component_digest_mismatch,distribution.manifest_invalid,distribution.missing_artifact_ref,distribution.missing_checksum",
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "path.preaccess_validation_order_violation"
    },
    {
      "category": "checksum",
      "description": "Every included Q47 file artifact has an exact checksum entry matching content_digest.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "no missing or wrong checksums",
      "id": "checksum.q47_values_match",
      "observed": {
        "included_names": [
          "CHANGELOG.preview.md",
          "RELEASE_NOTES.preview.md",
          "aide-lite-pack-v0.tar.gz",
          "aide-lite-pack-v0.zip",
          "install.md",
          "manifest.yaml",
          "release-provenance.json"
        ],
        "missing": [],
        "wrong": []
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "checksum",
      "description": "Checksum manifest digest matches the referenced file.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "sha256:d11f91599bbf13c39872b815b99a88063c50de8fcdf91aee76a09282bac2db06",
      "id": "checksum.manifest_digest_matches",
      "observed": "sha256:d11f91599bbf13c39872b815b99a88063c50de8fcdf91aee76a09282bac2db06",
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "checksum",
      "description": "Correct checksum filename with wrong checksum value fails.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "distribution.checksum_digest_mismatch",
      "id": "checksum.correct_name_wrong_value_refuses",
      "observed": {
        "codes": [
          "distribution.checksum_digest_mismatch"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "checksum",
      "description": "Missing checksum entry fails.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "distribution.missing_checksum",
      "id": "checksum.missing_entry_refuses",
      "observed": {
        "codes": [
          "distribution.missing_checksum"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "checksum",
      "description": "Two included artifacts with the same checksum basename fail.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "distribution.checksum_basename_collision",
      "id": "checksum.basename_collision_refuses",
      "observed": {
        "codes": [
          "distribution.checksum_basename_collision"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "checksum",
      "description": "Checksum algorithm must be exactly sha256.",
      "evidence_refs": [
        "checksum-value-review.md"
      ],
      "expected": "distribution.manifest_invalid",
      "id": "checksum.wrong_algorithm_refuses",
      "observed": {
        "codes": [
          "distribution.manifest_invalid"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "checksum.value_not_verified"
    },
    {
      "category": "protocol_range",
      "description": "protocol.min_above_v1_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.min_above_v1_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.max_below_v1_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.max_below_v1_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.inverted_range_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.inverted_range_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.malformed_range_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.malformed_range_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.missing_reader_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.missing_reader_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.missing_writer_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.missing_writer_refuses",
      "observed": {
        "codes": [
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.unsupported_migration_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.incompatible_migration",
      "id": "protocol.unsupported_migration_refuses",
      "observed": {
        "codes": [
          "distribution.incompatible_migration"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.unknown_required_feature_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unknown_required_feature",
      "id": "protocol.unknown_required_feature_refuses",
      "observed": {
        "codes": [
          "distribution.unknown_required_feature"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "protocol.component_incompatible_refuses must fail closed.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range",
      "id": "protocol.component_incompatible_refuses",
      "observed": {
        "codes": [
          "distribution.component_digest_mismatch",
          "distribution.unsupported_protocol_range"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "A future-major maximum must not be accepted merely because current v1 is inside the numeric interval.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range unless explicit future-major support exists",
      "id": "protocol.future_major_not_implicitly_accepted",
      "observed": {
        "codes": [],
        "range": {
          "max": "2.x",
          "min": "1.0.0"
        },
        "valid": true
      },
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "protocol_range",
      "description": "Unknown optional features are tolerated and preserved.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "valid with warning and preserved optional feature",
      "id": "protocol.unknown_optional_feature_tolerated",
      "observed": {
        "preserved": true,
        "valid": true,
        "warnings": [
          "unknown optional feature tolerated: future.optional.feature"
        ]
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "contamination",
      "description": "Forbidden source-state categories are classified, including export-pack target-root members under files/.",
      "evidence_refs": [
        "contamination-review.md"
      ],
      "expected": "observed forbidden reason for every independently forbidden path",
      "id": "contamination.forbidden_path_classification_complete",
      "observed": [
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide.local/",
          "path": ".aide.local/state.sqlite"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": ".env"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": "raw-prompt.txt"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": "raw-response.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/context/latest-",
          "path": ".aide/context/latest-task-packet.md"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/reports/",
          "path": ".aide/reports/distribution-manifest-v1/manifest.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/repo/latest-",
          "path": ".aide/repo/latest-inventory.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/roots/latest-",
          "path": ".aide/roots/latest-classification.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/tools/latest-",
          "path": ".aide/tools/latest-tools.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/install/latest-",
          "path": ".aide/install/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/repair/latest-",
          "path": ".aide/repair/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/upgrade/latest-",
          "path": ".aide/upgrade/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/rollback/latest-",
          "path": ".aide/rollback/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/uninstall/latest-",
          "path": ".aide/uninstall/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:logs/",
          "path": "logs/run.log"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.cache/",
          "path": ".cache/cache.bin"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:secrets/",
          "path": "secrets/token.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide.local/state.sqlite"
        },
        {
          "expected": "forbidden_exact",
          "observed": "secret_like_member",
          "path": "files/.env"
        },
        {
          "expected": "forbidden_exact",
          "observed": null,
          "path": "files/raw-prompt.txt"
        },
        {
          "expected": "forbidden_exact",
          "observed": null,
          "path": "files/raw-response.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/context/latest-task-packet.md"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/reports/distribution-manifest-v1/manifest.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/repo/latest-inventory.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/roots/latest-classification.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/tools/latest-tools.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/install/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/repair/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/upgrade/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/rollback/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/uninstall/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/logs/run.log"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.cache/cache.bin"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "secret_like_member",
          "path": "files/secrets/token.txt"
        }
      ],
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "contamination.forbidden_members_silently_filtered"
    },
    {
      "category": "contamination",
      "description": "Local-directory forbidden members are recorded instead of silently producing a clean digest.",
      "evidence_refs": [
        "contamination-review.md"
      ],
      "expected": "dirty and nested-dirty directories have forbidden members",
      "id": "contamination.directory_forbidden_members_recorded",
      "observed": {
        "clean_forbidden": 0,
        "dirty_forbidden": 1,
        "nested_dirty_forbidden": 0
      },
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "contamination.forbidden_members_silently_filtered"
    },
    {
      "category": "contamination",
      "description": "Manifest with reported local-directory forbidden members fails validation.",
      "evidence_refs": [
        "contamination-review.md"
      ],
      "expected": "distribution.source_state_contamination",
      "id": "contamination.directory_artifact_refuses",
      "observed": {
        "codes": [
          "distribution.source_state_contamination"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "contamination.forbidden_members_silently_filtered"
    },
    {
      "category": "fixture_coverage",
      "description": "Required valid and invalid fixture files exist.",
      "evidence_refs": [
        "fixture-coverage-review.md"
      ],
      "expected": "all required fixtures present",
      "id": "fixture.required_files_exist",
      "observed": {
        "missing_invalid": {},
        "missing_valid": {}
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "fixture.required_coverage_incomplete"
    },
    {
      "category": "fixture_coverage",
      "description": "Valid fixture corpus passes semantic validation.",
      "evidence_refs": [
        "fixture-coverage-review.md"
      ],
      "expected": "all valid fixtures valid",
      "id": "fixture.valid_behavior",
      "observed": {
        "full Q47/local archive": {
          "codes": [],
          "valid": true
        },
        "local directory": {
          "codes": [],
          "valid": true
        },
        "minimal valid unsigned": {
          "codes": [],
          "valid": true
        },
        "reordered equivalent": {
          "codes": [],
          "valid": true
        },
        "unknown optional extension round-trip": {
          "codes": [],
          "valid": true
        },
        "unknown optional feature": {
          "codes": [],
          "valid": true
        }
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "fixture.required_coverage_incomplete"
    },
    {
      "category": "fixture_coverage",
      "description": "Invalid fixture corpus fails semantic validation.",
      "evidence_refs": [
        "fixture-coverage-review.md"
      ],
      "expected": "all invalid fixtures invalid",
      "id": "fixture.invalid_behavior",
      "observed": {
        ".aide.local": {
          "codes": [
            "distribution.forbidden_member",
            "distribution.missing_checksum",
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "absolute path": {
          "codes": [
            "distribution.forbidden_member",
            "distribution.missing_checksum",
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "checksum basename collision": {
          "codes": [
            "distribution.checksum_basename_collision",
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "checksum missing": {
          "codes": [
            "distribution.missing_checksum"
          ],
          "valid": false
        },
        "checksum wrong value": {
          "codes": [
            "distribution.checksum_digest_mismatch",
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "dependency cycle": {
          "codes": [
            "distribution.component_dependency_cycle",
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "duplicate artifact_ref": {
          "codes": [
            "distribution.checksum_basename_collision",
            "distribution.duplicate_artifact"
          ],
          "valid": false
        },
        "duplicate component_id": {
          "codes": [
            "distribution.duplicate_component_id"
          ],
          "valid": false
        },
        "duplicate component_ref": {
          "codes": [
            "distribution.duplicate_component",
            "distribution.duplicate_component_id"
          ],
          "valid": false
        },
        "false signature verification": {
          "codes": [
            "distribution.signature_unverified"
          ],
          "valid": false
        },
        "forbidden member": {
          "codes": [
            "distribution.forbidden_member",
            "distribution.missing_checksum",
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "incompatible migration": {
          "codes": [
            "distribution.incompatible_migration"
          ],
          "valid": false
        },
        "inverted protocol range": {
          "codes": [
            "distribution.unsupported_protocol_range"
          ],
          "valid": false
        },
        "malformed digest": {
          "codes": [
            "distribution.artifact_digest_mismatch",
            "distribution.checksum_digest_mismatch",
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "missing SBOM": {
          "codes": [
            "distribution.sbom_unavailable"
          ],
          "valid": false
        },
        "missing artifact ref": {
          "codes": [
            "distribution.component_digest_mismatch",
            "distribution.missing_artifact_ref"
          ],
          "valid": false
        },
        "missing dependency": {
          "codes": [
            "distribution.component_digest_mismatch",
            "distribution.missing_component_dependency"
          ],
          "valid": false
        },
        "missing digest": {
          "codes": [
            "distribution.manifest_digest_mismatch"
          ],
          "valid": false
        },
        "signature placeholder false verified": {
          "codes": [
            "distribution.signature_unverified"
          ],
          "valid": false
        },
        "source contamination": {
          "codes": [
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "source report member": {
          "codes": [
            "distribution.forbidden_member",
            "distribution.missing_checksum",
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "traversal": {
          "codes": [
            "distribution.forbidden_member",
            "distribution.missing_checksum",
            "distribution.source_state_contamination"
          ],
          "valid": false
        },
        "unknown required feature": {
          "codes": [
            "distribution.unknown_required_feature"
          ],
          "valid": false
        },
        "unsupported protocol range": {
          "codes": [
            "distribution.unsupported_protocol_range"
          ],
          "valid": false
        },
        "unsupported source kind": {
          "codes": [
            "distribution.unsupported_source_kind"
          ],
          "valid": false
        },
        "wrong artifact digest": {
          "codes": [
            "distribution.artifact_digest_mismatch",
            "distribution.checksum_digest_mismatch",
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "wrong component digest": {
          "codes": [
            "distribution.component_digest_mismatch"
          ],
          "valid": false
        },
        "wrong distribution digest": {
          "codes": [
            "distribution.manifest_digest_mismatch"
          ],
          "valid": false
        },
        "wrong manifest payload digest": {
          "codes": [
            "distribution.manifest_digest_mismatch"
          ],
          "valid": false
        }
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "fixture.required_coverage_incomplete"
    },
    {
      "category": "fixture_coverage",
      "description": "Fixture corpus covers future-major protocol max declarations.",
      "evidence_refs": [
        "fixture-coverage-review.md"
      ],
      "expected": "direct invalid future-major protocol fixture",
      "id": "fixture.future_major_protocol_fixture_present",
      "observed": [],
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "fixture.required_coverage_incomplete"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.signature_unverified",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.signature_unverified",
      "id": "signature.false_verification_refuses",
      "observed": {
        "codes": [
          "distribution.signature_unverified"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "schema.optional_extension_boundary_missing"
    },
    {
      "category": "behavior_probe",
      "description": "Probe must fail with distribution.sbom_unavailable",
      "evidence_refs": [
        "validation-results.md"
      ],
      "expected": "distribution.sbom_unavailable",
      "id": "sbom.generated_claim_refuses",
      "observed": {
        "codes": [
          "distribution.sbom_unavailable"
        ],
        "valid": false
      },
      "outcome": "PASS",
      "severity": "info",
      "source_finding_id": "schema.optional_extension_boundary_missing"
    }
  ],
  "source_findings": [
    "schema.optional_extension_boundary_missing",
    "identity.mutable_status_changes_distribution_digest",
    "component.graph_integrity_not_validated",
    "artifact.integrity_metadata_not_validated",
    "path.preaccess_validation_order_violation",
    "checksum.value_not_verified",
    "protocol.range_semantics_incomplete",
    "contamination.forbidden_members_silently_filtered",
    "fixture.required_coverage_incomplete"
  ]
}
```
