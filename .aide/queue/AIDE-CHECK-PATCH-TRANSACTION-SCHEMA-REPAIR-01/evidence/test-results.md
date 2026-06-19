# Test Results

Focused PatchTransaction tests:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py
```

Result:

```text
Ran 31 tests
OK
```

The focused test count meets the repair baseline and includes direct coverage
for the drive-prefix and duplicate-normalization repairs.
