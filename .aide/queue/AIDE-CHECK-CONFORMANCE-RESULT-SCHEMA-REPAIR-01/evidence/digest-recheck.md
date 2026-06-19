# Digest Recheck

Status:

```text
PASS
```

Historical failed check preserved:

- failed recorded digest:
  `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`
- failed raw-profile digest reported by the original check:
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`
- historical finding: `profile_digest_mismatch`

Repair recheck:

- profile source: `.aide/reports/conformance-profile/profiles.json`
- profile ref: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- algorithm: `sha256-canonical-json-v1`
- independent digest:
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`
- repaired recorded digest:
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`
- repaired observation source digest:
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`

Independent calculation used:

```python
json.dumps(
    profile,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
).encode("utf-8")
```

Result:

```text
profile_digest_matches_pristine_profile: true
```

Negative checks:

- replacing the result profile digest with `sha256:000...000` fails validation;
- changing the pristine profile payload changes the digest;
- appending the lifecycle warning to a copied profile changes the copied digest
  and cannot validate the pristine-bound result.
