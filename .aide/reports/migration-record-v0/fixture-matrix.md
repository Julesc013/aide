# MigrationRecord v0 Fixture Matrix

- PASS `manual-review-ambiguous` -> `PASS_WITH_WARNINGS`
- PASS `no-op-compatibility` -> `PASS_WITH_WARNINGS`
- PASS `optional-extension-preserved` -> `PASS_WITH_WARNINGS`
- PASS `ambiguous-without-manual-review` -> `FAILED_VALIDATION`
- PASS `apply-claim` -> `FAILED_VALIDATION`
- PASS `destructive-without-rollback` -> `FAILED_VALIDATION`
- PASS `extension-required-unknown` -> `FAILED_VALIDATION`
- PASS `missing-input-digest` -> `FAILED_VALIDATION`
- PASS `missing-source-object` -> `FAILED_VALIDATION`
- PASS `output-digest-mismatch` -> `FAILED_VALIDATION`
- PASS `source-latest-output` -> `FAILED_VALIDATION`
- PASS `source-output-target-truth` -> `FAILED_VALIDATION`
- PASS `unknown-required-feature` -> `FAILED_VALIDATION`
