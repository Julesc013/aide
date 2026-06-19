# Artifact Digest Review

Status: `PASS`

Artifact locator:

```text
.aide/reports/patch-transaction/sample-unified.diff
```

Recorded digest:

```text
sha256:5747bd0d486a73c1b363b0f4c8af974b4ee1f24968a53221eba2c89f187b3c5f
```

Independent recomputation over the artifact bytes produced the same digest.
Changing the artifact bytes produced a different digest. Invalid digest shape
is rejected by validation.

The check does not require or claim a general diff parser, artifact resolver,
VCS reachability check, target existence check, base ancestry check, or clean
merge check.
