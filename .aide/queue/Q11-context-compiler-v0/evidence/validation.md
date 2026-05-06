# Q11 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 and Q10 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, action `unchanged`, 581 files.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q11 Context Compiler v0"`: PASS, action `unchanged`, 2,566 chars, 642 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 642 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, action `unchanged`.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 20 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

Final validation will be appended before review.
