# Test Results

Focused test command:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_conformance_result.py
```

Result:

```text
PASS
```

The focused test suite includes regression coverage for:

- profile digest matching the pristine accepted profile payload;
- lifecycle-warning mutation on a copy not becoming digest authority;
- profile digest changing when the pristine payload changes;
- projection and validation not mutating profile source;
- invalid profile digest failing validation;
- execution, runner, admission, and trust overclaims failing validation.
