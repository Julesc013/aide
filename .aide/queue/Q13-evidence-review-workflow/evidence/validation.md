# Q13 Validation Evidence

Interpreter used: Windows `py -3`.

## Final Validation

- `git status --short`: PASS, Q13-scoped changes only before final commit.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors; warnings are pre-existing review-gate/generated-manifest drift posture.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same structural warnings as validate.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 through Q13 are visible as `needs_review`, with report-only/no-provider/no-network posture.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, latest review packet present and under budget.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, `.aide/context/repo-snapshot.json`, 625 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, `.aide/context/repo-map.json`, `.aide/context/repo-map.md`, `.aide/context/test-map.json`, and `.aide/context/context-index.json`.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, `.aide/context/latest-context-packet.md`, 1,859 chars, 465 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS after removing transient Python `__pycache__` directories created by tests.
- `py -3 .aide/scripts/aide_lite.py verify --write-report .aide/verification/latest-verification-report.md`: PASS, report written with 0 warnings and 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, `.aide/context/latest-review-packet.md`, 7,643 chars, 1,911 approximate tokens, verifier result PASS.
- `py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md`: PASS after transient Python cache cleanup.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q14 Token Ledger and Savings Report"`: PASS, `.aide/context/latest-task-packet.md`, 3,224 chars, 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 7,643 chars, 143 lines, 1,911 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,224 chars, 104 lines, 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 28 tests.
- `git diff --check`: PASS; Git printed expected LF-to-CRLF working-copy warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template words, fake test strings, and path names; no actual provider key, credential, `.env` content, raw prompt log, or secret value was found.

## Transient Cache Cleanup

- Python test discovery created `__pycache__` directories under `.aide/scripts`, `core/compat`, and `core/harness`.
- Those generated cache directories were removed only after resolving paths and confirming they were inside the repository root.
- Final verifier runs after cleanup returned PASS.

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
