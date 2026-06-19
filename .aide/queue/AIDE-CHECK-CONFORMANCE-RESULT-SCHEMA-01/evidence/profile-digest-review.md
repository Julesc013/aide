# Profile Digest Review

Status:

```text
FAILED_VALIDATION
```

Recorded digest in `.aide/reports/conformance-result/results.json`:

```text
sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
```

Independently recomputed digest over raw
`.aide/reports/conformance-profile/profiles.json` using the repo stable JSON
format:

```text
sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d
```

These do not match.

Confirmed cause:

- `core/protocol/conformance_result.py` appends the warning
  `Profile lifecycle is candidate; result records observations but does not
  admit the subject.` to a loaded profile copy before hashing.
- The ConformanceResult validator recomputes the digest from the same mutated
  view.

This means the result digest does not bind the exact raw accepted profile report
payload. This is material because the check prompt requires exact profile
ref/version/digest binding.
