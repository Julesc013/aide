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
- absolute-path: true (FAILED_VALIDATION)
- aide-local-member: true (FAILED_VALIDATION)
- duplicate-artifact: true (FAILED_VALIDATION)
- duplicate-component: true (FAILED_VALIDATION)
- false-verified-signature: true (FAILED_VALIDATION)
- forbidden-source-report-member: true (FAILED_VALIDATION)
- incompatible-migration: true (FAILED_VALIDATION)
- missing-checksum: true (FAILED_VALIDATION)
- missing-digest: true (FAILED_VALIDATION)
- sbom-generated-claim: true (FAILED_VALIDATION)
- traversal-path: true (FAILED_VALIDATION)
- unknown-required-feature: true (FAILED_VALIDATION)
- unsupported-protocol: true (FAILED_VALIDATION)
- unsupported-source-kind: true (FAILED_VALIDATION)
- wrong-artifact-digest: true (FAILED_VALIDATION)
- wrong-manifest-digest: true (FAILED_VALIDATION)

## Warnings

- DistributionManifest v1 is proposed until independent check and acceptance.
- Q47 release artifacts remain local preview/no-publish evidence.
- No signature verification or SBOM generation is claimed.
