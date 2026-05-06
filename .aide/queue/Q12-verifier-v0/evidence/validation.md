# Q12 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09, Q10, and Q11 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, action `unchanged`, 594 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, action `unchanged`, 594 files, 542 test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,855 chars, 464 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q12 Verifier v0"`: PASS, action `unchanged`, 2,942 chars, 736 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 736 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 22 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Generation Note

- An early attempt to run `snapshot`, `index`, `context`, and `pack` concurrently produced one transient `snapshot` failure: `Expecting value: line 1 column 1 (char 0)`. The sequential workflow is the supported path and was rerun successfully before review.

## Final Validation Before Review

- `git status --short`: PASS, expected Q12 files modified/untracked before final evidence commit.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json`, 613 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo map, test map, and context index; 613 files and 559 heuristic test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,847 chars, 462 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q13 Evidence Review Workflow"`: PASS, `.aide/context/latest-task-packet.md`, 3,099 chars, 775 approximate tokens, budget PASS.
- `py -3 .aide/scripts/aide_lite.py verify --write-report .aide/verification/latest-verification-report.md`: PASS, wrote `.aide/verification/latest-verification-report.md`.
- `py -3 .aide/scripts/aide_lite.py verify --write-report .aide/verification/latest-verification-report.md`: PASS after evidence updates, 32 changed files, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/verification/latest-verification-report.md`: PASS, 4,178 chars, 99 lines, 1,045 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,099 chars, 102 lines, 775 approximate tokens.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors. Warnings are existing review-gate/generated-manifest drift posture.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS with the same known warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q12 is listed as `needs_review`.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, unchanged/current.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, unchanged/current on second run.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 30 checked files, 31 changed files, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --evidence .aide/queue/Q12-verifier-v0/evidence/verifier-report.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --changed-files`: PASS, all current changed files classify inside Q12 scope.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 21 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure because the hidden `.aide` start directory is not importable with this top-level discovery shape.
- `git diff --check`: PASS. Git emitted line-ending normalization notices only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template terms, section names, paths, and tests that construct fake strings at runtime; no actual provider key, credential, `.env` content, or secret value was found.

## Token Baseline Check

Naive baseline files counted for review-context comparison:

- `README.md`
- `ROADMAP.md`
- `AGENTS.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `.aide/queue/Q12-verifier-v0/prompt.md`
- `.aide/queue/Q12-verifier-v0/task.yaml`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md`

Combined baseline: 191,334 chars, 47,834 approximate tokens. Compact Q13 task packet plus latest verifier report: 7,277 chars, 1,820 approximate tokens. Estimated review-context reduction: about 96.2% by chars/4 approximation.

## Known Warnings

- Harness continues to report existing review gates for older raw queue statuses.
- Harness continues to report `.aide/generated/manifest.yaml` source-fingerprint drift; Q12 intentionally did not refresh generated artifacts.
- The hidden-directory unittest discovery command remains unsuitable for `.aide/scripts/tests`; direct discovery from `.aide/scripts/tests` passes and is the documented Q09-Q12 test path.
