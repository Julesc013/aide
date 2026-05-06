# Q16 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 through Q15 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, refreshed deterministic metadata snapshot with no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, refreshed repo-map/context-index metadata with no inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 1,930 chars / 483 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN only because baseline tests created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest review packet 6,222 chars / 1,556 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 48 current records, 49 total records, 0 budget warnings, 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, 49 records.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: WARN, 5 pass / 1 warn / 0 fail after review-packet regeneration.
- `py -3 .aide/scripts/aide_lite.py eval report`: WARN, 5 pass / 1 warn / 0 fail.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,223 chars / 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 6,222 chars / 1,556 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Final Validation

Pending.
