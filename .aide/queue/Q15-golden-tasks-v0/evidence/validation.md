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

## Implementation Validation

- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 tasks listed.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS after review packet refresh, 6 pass / 0 warn / 0 fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS after Q15 integration.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS with eval checks included.
- `py -3 .aide/scripts/tests/test_golden_tasks.py`: PASS, 9 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 45 tests.

## Final Validation Before Review

- `git status --short`: PASS, dirty only with intended Q15 changes and generated Q15/Q16 artifacts.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q15 shown as `needs_review`; no external calls, provider/model calls, network calls, or automatic worker invocation.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with `-t .`.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 45 tests.
- transient `__pycache__` directories from test imports were removed after resolving that targets stayed inside the repo.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, deterministic metadata only, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, deterministic repo-map/test-map/context-index, no inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 1,930 chars / 483 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 0 warnings, 0 errors after transient cache cleanup.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest Q15 review packet generated.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q16 Outcome Controller v0"`: PASS, latest Q16 task packet generated.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 6 pass / 0 warn / 0 fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 48 current records, 49 total records, 0 budget warnings, 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, totals include `eval_report`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,223 chars / 806 approximate tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 7,674 chars / 1,919 approximate tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `git diff --check`: PASS.
- targeted `rg` secret scan: PASS; matches were policy/test text only, not real secrets.

## Known Warnings

- Harness still reports historical review-gate nuance for Q00-Q03/Q05/Q06.
- Harness still reports stale `.aide/generated/manifest.yaml` source fingerprint.
- The hidden-directory unittest discovery shape with `-s .aide/scripts/tests -t .` remains a documented Python discovery limitation; direct discovery without `-t .` passes.
