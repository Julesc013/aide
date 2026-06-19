# AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Create and process a bounded repair task for
`AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

Repair only the material defect found by
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`:

```text
profile_digest_mismatch
```

Observed defect:

- `results.json` records profile digest
  `sha256:87c21ad142b05f1fe729a9d342287a6dcc60258c5af364e54501db5a6c64fef8`.
- Recomputing over the raw accepted profile report
  `.aide/reports/conformance-profile/profiles.json` gives
  `sha256:76da87d6325184fc1cd948e07068ff431b0fc075ab2f6e3a2a71b78ca5fadd7d`.
- The likely cause is that `load_accepted_conformance_profile` appends a
  lifecycle warning to an in-memory profile copy before `profile_digest` is
  computed, and validation recomputes the same mutated-view digest.

Repair scope:

- make the ConformanceResult profile digest bind the exact raw accepted
  ConformanceProfile payload, or explicitly materialize and identify any
  canonical normalized profile view before hashing;
- update helper validation so independent raw-profile digest mismatch fails;
- regenerate ConformanceResult reports;
- update focused tests to cover raw profile digest recomputation;
- preserve all no-runner, no-execution, no-collection, no-admission, no-trust,
  no-adapter, no-runtime, no-provider/network/Gateway/GitHub, no-target-apply,
  no-branch/worktree, no-release, and no-production boundaries.

Do not broaden into acceptance. After repair, recommend:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```
