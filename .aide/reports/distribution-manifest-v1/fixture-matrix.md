# DistributionManifest Fixture Matrix

| Case | Expected | Codes |
| --- | --- | --- |
| full-local-archive | PASS | none |
| local-directory | PASS | none |
| minimal-unsigned | PASS | none |
| reordered-input | PASS | none |
| absolute-path | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| aide-local-member | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| duplicate-artifact | FAILED_VALIDATION | distribution.duplicate_artifact |
| duplicate-component | FAILED_VALIDATION | distribution.duplicate_component |
| false-verified-signature | FAILED_VALIDATION | distribution.signature_unverified |
| forbidden-source-report-member | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| incompatible-migration | FAILED_VALIDATION | distribution.incompatible_migration |
| missing-checksum | FAILED_VALIDATION | distribution.missing_checksum |
| missing-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
| sbom-generated-claim | FAILED_VALIDATION | distribution.sbom_unavailable |
| traversal-path | FAILED_VALIDATION | distribution.forbidden_member, distribution.source_state_contamination |
| unknown-required-feature | FAILED_VALIDATION | distribution.unknown_required_feature |
| unsupported-protocol | FAILED_VALIDATION | distribution.unsupported_protocol_range |
| unsupported-source-kind | FAILED_VALIDATION | distribution.unsupported_source_kind |
| wrong-artifact-digest | FAILED_VALIDATION | distribution.artifact_digest_mismatch |
| wrong-manifest-digest | FAILED_VALIDATION | distribution.manifest_digest_mismatch |
