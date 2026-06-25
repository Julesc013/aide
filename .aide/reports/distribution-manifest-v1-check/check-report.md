# DistributionManifest v1 Independent Check

- result: REQUEST_CHANGES
- material_finding_count: 9
- missing_evidence: 0
- recommended_next_task: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01

## Material Findings

### schema.optional_extension_boundary_missing

- category: schema
- severity: material
- expected: Unknown optional extension fields should be preserved or tolerated through an explicit extension surface.
- observed: The root, metadata, spec, status, protocol, component, checksum, provenance, SBOM, and signature objects are closed with no extensions map; metadata optional extension would be rejected by schema.

### identity.mutable_status_changes_distribution_digest

- category: identity
- severity: material
- expected: Distribution identity should bind immutable distribution declaration, not review routing or implementation state.
- observed: Changing only these status fields changed the payload/distribution digest: recommended_next_task, status_status, proposed_capability, implementation_boolean

### component.graph_integrity_not_validated

- category: component
- severity: material
- expected: Corrupted component digests, missing artifact refs, unknown dependencies, duplicate component IDs, and cycles should fail closed.
- observed: The following malformed cases validated successfully: corrupt_component_content_digest, missing_artifact_ref, unknown_component_dependency, duplicate_component_id_different_ref, dependency_cycle

### artifact.integrity_metadata_not_validated

- category: artifact
- severity: material
- expected: Byte counts, media type, and compression declarations should be validated for included local archive artifacts.
- observed: The following malformed cases validated successfully: wrong_byte_count, wrong_media_type, wrong_compression_format

### path.preaccess_validation_order_violation

- category: path_safety
- severity: material
- expected: Malformed source artifact paths should be rejected before exists/stat/open/hash or traversal.
- observed: Source inspection shows path existence/stat/hash operations occur before any containment or forbidden-member validation in the release artifact projector.

### checksum.value_not_verified

- category: checksum
- severity: material
- expected: Checksum validation should verify algorithm, key uniqueness, and value equality with the artifact content digest.
- observed: A probe checksum manifest with the same artifact basename and a wrong digest value validated successfully.

### protocol.range_semantics_incomplete

- category: compatibility
- severity: material
- expected: Ranges should prove v1 inclusion, min <= max, required reader/writer fields, and coherent component constraints.
- observed: The following malformed compatibility cases validated successfully: lower_bound_above_v1, missing_min, missing_reader_version, missing_writer_version, incompatible_component_constraints

### contamination.forbidden_members_silently_filtered

- category: contamination
- severity: material
- expected: A contaminated distribution source should emit explicit contamination/refusal evidence or define a separate filtered-export proof boundary.
- observed: Source inspection shows directory inventory continues past forbidden members rather than recording a refusal.

### fixture.required_coverage_incomplete

- category: fixture
- severity: material
- expected: Required direct fixtures should exist for the distribution manifest contract and known risk matrix.
- observed: Missing fixture cases: duplicate-component-id, malformed-digest, wrong-component-digest, wrong-payload-digest, wrong-distribution-digest, missing-artifact-ref, missing-dependency, dependency-cycle, unsupported-source, unknown-optional-feature, unsupported-protocol-range, inverted-protocol-range, forbidden-member, source-contamination, checksum-missing, checksum-wrong-value, checksum-basename-collision, signature-placeholder, false-signature-verification, missing-sbom, unknown-optional-extension-round-trip
