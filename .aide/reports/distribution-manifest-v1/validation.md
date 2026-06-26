# DistributionManifest v1 Validation

- result: PASS_WITH_WARNINGS
- proposed_capability: distribution_manifest_v1
- recommended_next_task: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01

## Checks

- schema_exists: true
- helper_exists: true
- cli_registered: true
- manifest_generated: true
- manifest_valid: true
- schema_alignment: true
- fixture_matrix_passed: true
- reordered_input_same_digest: true
- q47_release_bundle_mapped: true
- q48_not_distribution_truth: true
- install_apply_not_implemented: true
- release_publication_not_implemented: true
- target_repository_mutation_not_implemented: true
- network_calls_not_implemented: true
- provider_model_calls_not_implemented: true
- absolute_local_paths_suppressed: true

## Fixture Results

- full-local-archive: true (PASS)
- local-directory: true (PASS)
- minimal-unsigned: true (PASS)
- reordered-input: true (PASS)
- signature-placeholder: true (PASS)
- unknown-optional-extension-round-trip: true (PASS)
- unknown-optional-feature: true (PASS)
- absolute-path: true (FAILED_VALIDATION)
- aide-local-member: true (FAILED_VALIDATION)
- checksum-basename-collision: true (FAILED_VALIDATION)
- checksum-missing: true (FAILED_VALIDATION)
- checksum-wrong-value: true (FAILED_VALIDATION)
- component-protocol-future-major: true (FAILED_VALIDATION)
- dependency-cycle: true (FAILED_VALIDATION)
- duplicate-artifact: true (FAILED_VALIDATION)
- duplicate-component-id: true (FAILED_VALIDATION)
- duplicate-component: true (FAILED_VALIDATION)
- false-signature-verification: true (FAILED_VALIDATION)
- false-verified-signature: true (FAILED_VALIDATION)
- forbidden-member: true (FAILED_VALIDATION)
- forbidden-source-report-member: true (FAILED_VALIDATION)
- incompatible-migration: true (FAILED_VALIDATION)
- inverted-protocol-range: true (FAILED_VALIDATION)
- malformed-digest: true (FAILED_VALIDATION)
- missing-artifact-ref: true (FAILED_VALIDATION)
- missing-checksum: true (FAILED_VALIDATION)
- missing-dependency: true (FAILED_VALIDATION)
- missing-digest: true (FAILED_VALIDATION)
- missing-sbom: true (FAILED_VALIDATION)
- protocol-range-max-2-0-0: true (FAILED_VALIDATION)
- protocol-range-max-2x: true (FAILED_VALIDATION)
- protocol-range-min-2-0-0: true (FAILED_VALIDATION)
- sbom-generated-claim: true (FAILED_VALIDATION)
- source-contamination: true (FAILED_VALIDATION)
- traversal-path: true (FAILED_VALIDATION)
- unknown-required-feature: true (FAILED_VALIDATION)
- unsupported-protocol-range: true (FAILED_VALIDATION)
- unsupported-protocol: true (FAILED_VALIDATION)
- unsupported-source-kind: true (FAILED_VALIDATION)
- unsupported-source: true (FAILED_VALIDATION)
- wrong-artifact-digest: true (FAILED_VALIDATION)
- wrong-component-digest: true (FAILED_VALIDATION)
- wrong-distribution-digest: true (FAILED_VALIDATION)
- wrong-manifest-digest: true (FAILED_VALIDATION)
- wrong-payload-digest: true (FAILED_VALIDATION)

## Warnings

- DistributionManifest v1 is proposed until independent check and acceptance.
- Q47 release artifacts remain local preview/no-publish evidence.
- No signature verification or SBOM generation is claimed.
