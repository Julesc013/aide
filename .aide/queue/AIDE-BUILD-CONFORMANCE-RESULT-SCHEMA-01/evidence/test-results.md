# Test Results

Focused tests run:

```text
py -3 -m py_compile core/protocol/conformance_result.py
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
```

Observed result:

```text
Ran 18 tests
OK
```

Coverage includes schema parsing, deterministic projection, profile binding,
profile digest mismatch, result/admission boundary independence, case-result
semantics, aggregation precedence, optional/advisory warning behavior, CLI
dispatch, forbidden subcommand rejection, and no-overclaiming report text.
