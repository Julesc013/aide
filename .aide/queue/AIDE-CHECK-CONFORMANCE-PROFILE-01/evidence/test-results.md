# Test Results

Result: `PASS`

Commands run:

```text
py -3 -m py_compile core/protocol/conformance_profile.py .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_profile.py
```

Focused unittest result:

```text
Ran 17 tests in 2.511s
OK
```
