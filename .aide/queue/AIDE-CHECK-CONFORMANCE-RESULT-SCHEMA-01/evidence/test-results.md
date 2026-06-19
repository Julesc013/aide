# Test Results

Status:

```text
PASS_WITH_FINDING
```

Build task focused tests were rerun during preflight:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
```

Observed result:

```text
18 tests passed
```

The existing tests do not catch the raw-profile digest mismatch because helper
validation recomputes the digest over the same mutated in-memory profile view.
The repair task should add explicit raw profile digest recomputation coverage.
