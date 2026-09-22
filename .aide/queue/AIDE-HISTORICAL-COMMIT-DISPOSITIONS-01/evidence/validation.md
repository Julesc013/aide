# Validation

- `py -3 -B .aide/scripts/tests/test_q27_commit_recovery.py -v`: PASS, 19 tests.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_q27_commit_recovery.py`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py eval run --task commit_message_standard_golden`: PASS, 22/22 checks; generated latest-run reports were restored because they are outside task scope.
- Raw range checks for `bfb86c12^!` and `486e81cd^!`: FAIL with the exact retained failures recorded in `raw-policy-failures.md`.
- Default range checks for both proposed records: FAIL with `disposition_status: proposed` and `disposition is proposed and has no effect`.
- `py -3 -B .aide/scripts/aide_lite.py pack-status`: PASS for the predecessor pack; a clean-source refresh is still required to carry the new portable policy, schema, helper, and docs.
- `git diff --check`: PASS for the current source change.
