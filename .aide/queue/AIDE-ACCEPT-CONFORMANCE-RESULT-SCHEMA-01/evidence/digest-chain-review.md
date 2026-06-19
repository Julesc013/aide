# Digest Chain Review

Status:

```text
PASS
```

Historical failed check:

- recorded ConformanceResult digest:
  `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`
- failed-check raw-profile digest:
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`
- result: `FAILED_VALIDATION`

Accepted repaired digest:

- algorithm: `sha256-canonical-json-v1`
- source: pristine accepted ConformanceProfile payload
- profile ref: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- accepted digest:
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`

Repair-check confirmations:

- repaired recorded digest matches independent pristine-profile digest;
- `source_profile_digest` matches the same digest;
- bad digest fails validation;
- lifecycle-warning mutation on a copy cannot become digest authority;
- projection is deterministic;
- profile source is not mutated.
