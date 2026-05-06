# Q10 Validation Evidence

Interpreter used: Windows `py -3` with Python 3.11.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors; recommended Q09 review.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 17 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Implementation Checks

- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS; initially reported legacy Q09 AGENTS token-survival marker before `adapt`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS; initially warned that AGENTS token-survival guidance was legacy before `adapt`.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 20 tests after AIDE Lite test updates.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 10 tests.
- `py -3 scripts/aide compile --write`: PASS_WITH_WARNINGS; refreshed `.aide/generated/manifest.yaml` through reviewed Harness machinery after queue/catalog changes.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `git diff --check`: PASS. Git printed line-ending normalization warnings only.

## Final Validation

- `git status --short`: PASS for expected remaining Q10 evidence/context modifications before final evidence commit.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors; still recommends Q09 review because Q09 raw status remains `needs_review`.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q10 appears as `needs_review`, generated manifest fingerprint is current, and no external/model/provider/network/worker calls are reported.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 20 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS; Q09 and Q10 statuses are visible, snapshot and latest packet exist, adapter status is current.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS; latest packet is 642 approximate tokens and AGENTS managed section is current.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS; action `unchanged` during the final command set, 581 files, no inline contents. A later evidence-refresh run wrote updated hashes after evidence files changed.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q11 Context Compiler v0"`: PASS; action `written` after packet warning-list formatting was tightened, 2,566 chars, 642 approximate tokens, budget status PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 2,566 chars, 91 lines, 642 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS; action `unchanged`, before/after status `current`.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS; second run action `unchanged`, proving no-diff behavior.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: EXPECTED FAIL; Python reports `Start directory is not importable` for hidden `.aide/scripts/tests` when using top-level package discovery.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 10 tests. This is the documented Q10 direct discovery form.
- `git diff --check`: PASS. Git printed line-ending normalization warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template words such as `TOKEN`, `SECRET_PATTERNS`, and path names; no actual provider key, credential, `.env` content, or secret value was found.

## Known Warnings

- Harness warnings are the existing review-gate warnings for Q00-Q03, Q05, and Q06 raw statuses.
- Harness doctor still recommends Q09 review because Q09 remains `needs_review`; Q10 proceeds only by explicit prompt authorization and also stops at review.
- `.aide/scripts/tests` works with direct unittest discovery but not with `-t .` hidden-directory top-level discovery.
