# Fixture Matrix

Valid fixtures:

- `minimal-unsigned`
- `full-local-archive`
- `local-directory`
- `reordered-input`

Invalid fixtures:

- `absolute-path`
- `aide-local-member`
- `duplicate-artifact`
- `duplicate-component`
- `false-verified-signature`
- `forbidden-source-report-member`
- `incompatible-migration`
- `missing-checksum`
- `missing-digest`
- `sbom-generated-claim`
- `traversal-path`
- `unknown-required-feature`
- `unsupported-protocol`
- `unsupported-source-kind`
- `wrong-artifact-digest`
- `wrong-manifest-digest`

The live validation report records every fixture result and expected refusal
subset under `.aide/reports/distribution-manifest-v1/validation.json`.
