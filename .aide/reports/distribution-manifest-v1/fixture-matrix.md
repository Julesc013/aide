# DistributionManifest Fixture Matrix

| Case | Expected | Codes |
| --- | --- | --- |
| full-local-archive | PASS | none |
| local-directory | PASS | none |
| minimal-unsigned | PASS | none |
| reordered-input | PASS | none |
| signature-placeholder | PASS | none |
| unknown-optional-extension-round-trip | PASS | none |
| unknown-optional-feature | PASS | none |
| absolute-path | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| aide-local-member | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| checksum-basename-collision | FAILED_VALIDATION | distribution.checksum_basename_collision |
| checksum-missing | FAILED_VALIDATION | distribution.missing_checksum |
| checksum-wrong-value | FAILED_VALIDATION | distribution.checksum_digest_mismatch |
| component-protocol-future-major | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| dependency-cycle | FAILED_VALIDATION | distribution.component_dependency_cycle |
| duplicate-artifact | FAILED_VALIDATION | distribution.duplicate_artifact |
| duplicate-component-id | FAILED_VALIDATION | distribution.duplicate_component_id |
| duplicate-component | FAILED_VALIDATION | distribution.duplicate_component |
| false-signature-verification | FAILED_VALIDATION | distribution.signature_unverified |
| false-verified-signature | FAILED_VALIDATION | distribution.signature_unverified |
| forbidden-member | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| forbidden-source-report-member | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| incompatible-migration | FAILED_VALIDATION | distribution.incompatible_migration |
| inverted-protocol-range | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| malformed-digest | FAILED_VALIDATION | distribution.artifact_digest_mismatch |
| missing-artifact-ref | FAILED_VALIDATION | distribution.missing_artifact_ref |
| missing-checksum | FAILED_VALIDATION | distribution.missing_checksum |
| missing-dependency | FAILED_VALIDATION | distribution.missing_component_dependency |
| missing-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
| missing-sbom | FAILED_VALIDATION | distribution.sbom_unavailable |
| protocol-range-max-2-0-0 | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| protocol-range-max-2x | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| protocol-range-min-2-0-0 | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| sbom-generated-claim | FAILED_VALIDATION | distribution.sbom_unavailable |
| source-contamination | FAILED_VALIDATION | distribution.source_state_contamination |
| traversal-path | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| unknown-required-feature | FAILED_VALIDATION | distribution.unknown_required_feature |
| unsupported-protocol-range | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| unsupported-protocol | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| unsupported-source-kind | FAILED_VALIDATION | distribution.unsupported_source_kind |
| unsupported-source | FAILED_VALIDATION | distribution.unsupported_source_kind |
| wrong-artifact-digest | FAILED_VALIDATION | distribution.artifact_digest_mismatch |
| wrong-component-digest | FAILED_VALIDATION | distribution.component_digest_mismatch |
| wrong-distribution-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
| wrong-manifest-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
| wrong-payload-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
