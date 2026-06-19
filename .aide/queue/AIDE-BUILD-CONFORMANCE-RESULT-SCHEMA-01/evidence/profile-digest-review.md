# Profile Digest Review

The result records a stable SHA-256 digest of the bound ConformanceProfile
payload:

```text
sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8
```

Validation recomputes the digest from the loaded profile and fails if the result
digest diverges.

The digest identifies the observed profile payload; it does not admit the
subject or prove capability trust.
