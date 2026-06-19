# Test Results

Commands run:

```text
py -3 -m py_compile core/protocol/patch_transaction.py .aide/scripts/tests/test_aide_patch_transaction.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py
```

Results:

- compile: `PASS`
- focused PatchTransaction tests: `PASS`, 24 tests

The suite includes regression coverage for the two material path-scope findings.
