# Refusal Matrix

Implemented refusal codes:

- `distribution.manifest_missing`
- `distribution.manifest_invalid`
- `distribution.manifest_digest_mismatch`
- `distribution.duplicate_component`
- `distribution.duplicate_artifact`
- `distribution.artifact_digest_mismatch`
- `distribution.unsupported_protocol_range`
- `distribution.unknown_required_feature`
- `distribution.unsupported_source_kind`
- `distribution.forbidden_member`
- `distribution.source_state_contamination`
- `distribution.signature_unverified`
- `distribution.sbom_unavailable`
- `distribution.missing_checksum`
- `distribution.incompatible_migration`

The fixture matrix exercises the material refusal families required for this
first build.
