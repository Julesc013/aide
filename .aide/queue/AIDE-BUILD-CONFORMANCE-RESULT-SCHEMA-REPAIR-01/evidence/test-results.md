# Test Results

Focused tests:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
Ran 22 tests
OK
```

The suite covers independent digest recomputation, digest mismatch failure,
mutation-copy failure, payload-change digest changes, projection determinism,
profile source immutability, aggregation semantics, case-result validation,
CLI dispatch, and no-overclaiming boundaries.
