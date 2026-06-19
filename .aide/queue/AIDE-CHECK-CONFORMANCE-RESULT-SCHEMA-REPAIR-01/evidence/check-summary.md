# Check Summary

Result:

```text
PASS_WITH_WARNINGS
```

The independent recheck confirms that
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01` repaired the material
ConformanceResult profile digest defect.

Confirmed:

- The historical failed check remains preserved.
- The repaired result records profile ref
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.
- The repaired recorded digest is
  `sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70`.
- Independent `hashlib.sha256` over the pristine accepted profile payload using
  `sha256-canonical-json-v1` gives the same digest.
- Bad profile digests fail validation.
- Lifecycle-warning mutation on a copy does not become authoritative digest
  source.
- Projection is deterministic and does not mutate the profile source.
- Case results, aggregate outcome, execution, admission, subject admission, and
  trust boundaries remain unchanged.

Recommended next task:

```text
AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01
```
