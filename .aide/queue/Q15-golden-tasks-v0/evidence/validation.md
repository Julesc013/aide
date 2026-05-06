# Q15 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 through Q14 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json`, 641 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo-map and context-index, 641 files, 584 test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,893 chars, 474 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN only because baseline test discovery created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, `.aide/context/latest-review-packet.md`, 5,963 chars, 1,491 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 41 records, 0 budget warnings, 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, 41 records.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,211 chars, 104 lines, 803 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 5,963 chars, 117 lines, 1,491 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

Final validation will be appended before review.
