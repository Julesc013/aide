# Tests

Commands:

```bash
py -3 -m py_compile core/protocol/context_pack_v2.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_context_pack_v2.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_context_pack_v2.py
```

Results:

- Python compilation: passed
- Focused ContextPack v2 tests: 13 passed

The focused tests cover schema parsing, stable identity, deterministic
projection, source immutability, required sections, wrong-kind refs,
source-existence and digest validation, no-execution status flags, unknown
required capabilities, explicit non-capabilities, and CLI dispatch.
