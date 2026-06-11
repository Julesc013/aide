# Test Results

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py core/apply/lifecycle_fixture_runner.py` | PASS | CLI and runner module compile. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 12 focused tests passed. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | 37 existing apply tests passed. |

Coverage warning:

- Existing tests cover unsupported scenario, unsupported mode, parent traversal,
  absolute path, symlink escape where platform-supported, report aliases,
  rollback non-execution, and CLI dispatch boundary.
- Existing tests do not directly exercise `ScopedExecutor.apply` with an
  unsupported operation type. The code rejects it, but HARDEN-01 should add the
  direct regression test.
