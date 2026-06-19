# AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
# Independent Recheck of Canonical ConformanceProfile Digest Repair

Create and process `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Independently review:

- `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`
- `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`
- `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`

Do not overwrite or supersede the historical failed check.

Scope:

- check only
- no repair
- no schema/helper/test changes
- no runner
- no execution
- no automatic collection
- no profile activation
- no admission or trust
- no PatchTransaction
- no runtime or external calls

Verify independently:

1. reproduce the original digest mismatch from historical evidence
2. load the pristine accepted profile payload directly
3. select the exact profile by profile_ref
4. calculate SHA-256 independently without importing the production digest helper
5. compare the independent digest to the repaired result digest
6. require exact equality
7. verify the production helper does not mutate its profile input
8. verify validation uses pristine profile source
9. verify lifecycle-warning mutation on a copy cannot alter the authoritative digest
10. verify incorrect digest fails validation
11. verify profile payload change changes the digest
12. verify repeated projection is deterministic
13. verify accepted profile and predecessor artifacts remain unchanged
14. verify case outcomes and aggregate semantics did not change to conceal the defect
15. verify execution/admission/trust remain false
16. run focused tests and predecessor validators
17. verify reports parse
18. verify no secrets or forbidden operations

Expected result:

```text
PASS
or
PASS_WITH_WARNINGS
```

Recommended next task if the recheck passes:

```text
AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01
```

If the digest remains incorrect:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-02
```
