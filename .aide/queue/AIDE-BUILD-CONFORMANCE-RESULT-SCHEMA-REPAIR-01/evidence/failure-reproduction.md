# Failure Reproduction

Historical failed check:

- task_id: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
- result: FAILED_VALIDATION
- finding: profile_digest_mismatch

Before repair:

- recorded result digest: sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
- failed-check raw-profile digest using prior pretty JSON check: sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d
- independent pristine digest using `sha256-canonical-json-v1`: sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70
- mismatch reproduced: true

The prior validator reported `profile_digest_matches: true` because it compared
the result digest to the same mutated in-memory profile representation.
