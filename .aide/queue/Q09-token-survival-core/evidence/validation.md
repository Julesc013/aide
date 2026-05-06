# Q09 Validation Evidence

Interpreter used throughout: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, Q08 shown as passed with PASS_WITH_NOTES.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 10 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Implementation Validation

- `py -3 scripts/aide compile --write`: PASS. Refreshed generated AGENTS managed summary and `.aide/generated/manifest.yaml` through the reviewed Harness write path.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS after fixing root dot-path matching.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS; before `adapt`, it warned that AGENTS token-survival guidance and latest task packet were missing.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL as an attempted preferred-path check. Python unittest cannot import hidden `.aide` as a package with `-t .`; tests were relocated to `core/harness/tests/test_aide_lite.py`.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS before relocation, 7 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS after relocation, 17 tests.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json` with 569 files and no inline contents.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q10 AIDE Lite hardening"`: PASS, wrote `.aide/context/latest-task-packet.md`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 2587 chars, 100 lines, 647 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS; first run updated AGENTS, second run reported unchanged.

## Final Validation Before Review

- `py -3 scripts/aide compile --write`: PASS. Manifest source fingerprint current after Q09 final status/doc changes.
- `py -3 scripts/aide self-check --write-report`: PASS_WITH_WARNINGS, wrote non-canonical `.aide/runs/self-check/latest.md`; Q09 shown as `needs_review`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors; next step is Q09 review.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, 149 info, 6 warnings, 0 errors; no provider/model/network calls.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 17 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, 569 files, contents inline false.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q10 AIDE Lite hardening"`: PASS, 2587 chars, 647 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 2587 chars, 100 lines, 647 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, unchanged.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `git diff --check`: PASS with line-ending normalization warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template words such as `TOKEN`, `SECRET_PATTERNS`, and path names; no actual provider key, credential, `.env` content, or secret value was found.

## Known Warnings

- Harness warnings are review-gate nuance for Q00-Q03 and Q05/Q06 raw statuses.
- Q09 itself is intentionally at `needs_review`.
- `.aide/scripts/tests` with `unittest -t .` is not viable because hidden `.aide` is not an importable package path; Q09 tests live under `core/harness/tests`.
