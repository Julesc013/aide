# Test Results

Focused tests after check artifacts were generated:

```powershell
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m py_compile core/protocol/capability_manifest.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_capability_manifest.py
```

Result:

```text
Ran 11 tests in 12.761s
OK
```

Preflight checks already completed:

- `capability-manifest status`: PASS_WITH_WARNINGS
- `capability-manifest project`: PASS_WITH_WARNINGS
- `capability-manifest validate`: PASS_WITH_WARNINGS
- predecessor validators: PASS or PASS_WITH_WARNINGS
- unsupported `capability-manifest run/execute/admit/conformance/adapter-run/repair/mutate`: fail closed with exit code 2
