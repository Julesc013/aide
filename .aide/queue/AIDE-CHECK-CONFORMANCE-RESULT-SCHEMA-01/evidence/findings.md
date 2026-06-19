# Findings

## ERROR: profile_digest_mismatch

The ConformanceResult records:

```text
sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
```

Independent recomputation over the raw accepted profile report
`.aide/reports/conformance-profile/profiles.json` gives:

```text
sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d
```

This is material because the check gate requires exact profile ref, version,
digest, and subject binding.

Disposition:

```text
requires_bounded_repair
```

Recommended task:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```
