# Test Results

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 -m py_compile .aide\scripts\aide_lite.py core\apply\lifecycle_fixture_runner.py` | PASS | CLI and runner module compile. |
| `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_lifecycle_fixture_runner.py` | PASS | 12 focused tests passed, including report aliases, unsupported scenario/mode fail-closed behavior, rollback non-execution, and dispatch boundary checks. |
| `py -3 -m unittest core.apply.tests.test_transaction_executor core.apply.tests.test_managed_sections` | PASS | Existing apply/managed-section suites passed in the build turn and remain part of final validation. |

Deferred broad tests:

- No provider, Gateway, service, Commander, branch/worktree, release, or target-repo tests were run because those capabilities are out of scope for this WorkUnit.
