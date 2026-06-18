# Test Results

Focused validation run:

```text
py -3 -m py_compile core/protocol/conformance_profile.py
PASS

py -3 -m py_compile .aide/scripts/aide_lite.py
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_profile.py
Ran 17 tests in 2.175s
OK

py -3 .aide/scripts/aide_lite.py conformance-profile project
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py conformance-profile validate
PASS_WITH_WARNINGS
```

Broader validation results are recorded in `validation.md`.
