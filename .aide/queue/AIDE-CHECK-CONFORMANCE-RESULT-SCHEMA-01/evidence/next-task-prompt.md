# AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Create and process a bounded repair task for:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```

Repair only the material defect found by:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
```

Defect:

```text
profile_digest_mismatch
```

Observed:

- recorded ConformanceResult profile digest:
  `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`
- independently recomputed raw profile digest:
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`

Repair requirements:

- ensure the result digest binds the exact raw accepted ConformanceProfile
  payload, or explicitly define and materialize a canonical normalized profile
  view before hashing;
- make validation fail when raw accepted profile digest and recorded digest
  diverge;
- add focused tests that catch this mismatch;
- regenerate ConformanceResult reports and task evidence;
- preserve no-runner, no-execution, no-collection, no-profile-activation,
  no-admission, no-trust, no-adapter, no-runtime, no-provider/network/Gateway,
  no-GitHub, no-target-apply, no-branch/worktree, no-release, and
  no-production boundaries.

Recommended next after repair:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```
