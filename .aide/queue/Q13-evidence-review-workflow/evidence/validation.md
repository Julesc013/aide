# Q13 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09, Q10, Q11, and Q12 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json`, 613 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo-map and context-index, 613 files, 559 test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,847 chars, 462 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q13 Evidence Review Workflow"`: PASS, `.aide/context/latest-task-packet.md`, 3,099 chars, 775 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN only because test runs created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md`: WARN with the same transient-cache findings.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

Final validation will be appended before review.
