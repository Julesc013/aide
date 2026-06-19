# Test Results

Focused tests:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py
```

Result:

```text
Ran 22 tests
OK
```

Coverage includes valid minimal record, stable ReferenceID form, deterministic
projection, source immutability, missing/invalid refs, digest shape and digest
binding, fail-closed path scope, no-apply/no-target-mutation consistency,
approval/trust overclaim rejection, lifecycle consistency, and explicit
non-capability preservation.
