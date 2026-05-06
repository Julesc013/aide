# Q18 Validation

## Baseline Validation Before Editing

- `git status --short`: PASS, clean before baseline command refreshes.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info / 7 warnings / 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same known warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, report-only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with one known Q17 validation-evidence near-budget token-ledger warning.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS.
- `py -3 .aide/scripts/aide_lite.py index`: PASS.
- `py -3 .aide/scripts/aide_lite.py context`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS with one known near-budget evidence warning.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS with one known near-budget evidence warning.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 6 pass / 0 warn / 0 fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, packet_too_large warning from existing Q17 evidence near-budget status.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, top recommendation `REC-PACKET-BUDGET`.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory `frontier` route with `architecture_decision` hard floor.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3486 chars / 872 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 5226 chars / 1307 approximate tokens after baseline refresh.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL with known hidden `.aide` importability behavior.

Baseline generated-file churn was restored before Q18 edits began.

## Final Validation

Pending.
