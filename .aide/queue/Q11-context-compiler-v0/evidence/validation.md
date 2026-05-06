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

## Final Validation Before Review

- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json`, 594 files, aggregate 424,168 approximate tokens, no contents inlined.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo-map/context-index outputs, 594 repo-map records, 542 test-map mappings, source snapshot hash `8db626ea4901201d81043132ea937e8721e210d0c1cfa452a563b574aa08b744`.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,855 chars, 464 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q12 Verifier v0"`: PASS, `.aide/context/latest-task-packet.md` unchanged, 2,942 chars, 736 approximate tokens, budget PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-context-packet.md`: PASS, 1,855 chars, 80 lines, 464 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 2,942 chars, 99 lines, 736 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, `AGENTS.md` unchanged and managed section current.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, second run unchanged; deterministic adapter behavior confirmed.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 12 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 22 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors. Warnings are existing review gates plus generated manifest source fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same warning posture as validate.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, report-only; Q09/Q10/Q11 remain `needs_review`; generated manifest drift remains visible.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: EXPECTED FAIL, hidden `.aide` start directory is not importable with this top-level discovery shape. Direct discovery without `-t .` and the Harness mirror tests pass.
- `git diff --check`: PASS, no whitespace errors. Git reported line-ending normalization warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template strings such as `TOKEN`, `SECRET_PATTERNS`, `api_key`, and path names; no actual provider key, credential, `.env` content, or secret value was found.
- `git status --short`: PASS, only intended Q11 files remained modified/untracked after removing Python `__pycache__` directories.

## Known Warnings

- `.aide/generated/manifest.yaml` source fingerprint drift remains visible and was not refreshed in Q11.
- Q00-Q03/Q05/Q06/Q09/Q10/Q11 review-gate statuses remain visible according to their queue records.
- Direct unittest discovery with `-t .` cannot import the hidden `.aide` start directory; supported test paths passed.
