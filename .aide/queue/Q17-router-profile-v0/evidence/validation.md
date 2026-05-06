# Q17 Validation

## Baseline Validation Before Editing

- `git status --short`: PASS, clean before baseline command refreshes.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info / 7 warnings / 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS.
- `py -3 .aide/scripts/aide_lite.py index`: PASS.
- `py -3 .aide/scripts/aide_lite.py context`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: PASS.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL with known hidden `.aide` start-directory importability behavior.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Final Validation

Pending.
