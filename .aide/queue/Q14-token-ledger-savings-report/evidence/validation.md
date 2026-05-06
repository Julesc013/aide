# Q14 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 through Q13 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote `.aide/context/repo-snapshot.json`, 625 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo-map and context-index, 625 files, 570 test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote `.aide/context/latest-context-packet.md`, 1,859 chars, 465 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN only because baseline test runs created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, `.aide/context/latest-review-packet.md`, 7,244 chars, 1,811 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,224 chars, 104 lines, 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 7,244 chars, 131 lines, 1,811 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Final Validation

- `git status --short`: PASS, Q14-scoped modified/untracked files only before final commit.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors. Warnings are existing review-gate/generated-manifest drift posture.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same structural warnings as validate; next recommended step still points to Q09 review because older raw queue statuses remain review-gated.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09-Q14 visible as `needs_review`; report-only/no-provider/no-network posture preserved.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS; Q14 ledger artifacts and 41 ledger records found.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with one token-ledger warning: latest review packet is near budget at 1,946/2,400 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, `.aide/context/repo-snapshot.json`, 641 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, regenerated repo-map/context-index, 641 files, 584 test mappings, no inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, `.aide/context/latest-context-packet.md`, 1,893 chars, 474 approximate tokens, `within_budget`.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS after removing transient Python `__pycache__` directories created by tests.
- `py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md`: PASS after transient cache cleanup.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, `.aide/context/latest-review-packet.md`, 7,784 chars, 1,946 approximate tokens, verifier result PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, wrote 40 current records, 41 total records, one near-budget review-packet warning, zero regression warnings, raw prompt/response storage false.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, `.aide/reports/token-savings-summary.md` unchanged after scan, 41 records, one budget warning, zero regression warnings.
- `py -3 .aide/scripts/aide_lite.py ledger compare --baseline root_history_baseline --file .aide/context/latest-task-packet.md`: PASS, 803 vs 49,008 approximate tokens, 98.4 percent estimated reduction.
- `py -3 .aide/scripts/aide_lite.py ledger compare --baseline review_baseline --file .aide/context/latest-review-packet.md`: PASS, 1,946 vs 6,876 approximate tokens, 71.7 percent estimated reduction.
- `py -3 .aide/scripts/aide_lite.py ledger compare --baseline repo_context_baseline --file .aide/context/latest-context-packet.md`: PASS, 474 vs 52,772 approximate tokens, 99.1 percent estimated reduction.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q15 Golden Tasks v0"`: PASS, `.aide/context/latest-task-packet.md`, 3,211 chars, 803 approximate tokens, `within_budget`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,211 chars, 104 lines, 803 approximate tokens, `within_budget`.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 7,784 chars, 135 lines, 1,946 approximate tokens, `near_budget`.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 36 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `git diff --check`: PASS; Git printed expected LF-to-CRLF working-copy warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/template terms, fake test strings, section names, and path names; no actual provider key, credential, `.env` content, raw prompt log, or secret value was found.

## Cleanup

Python test execution created transient `__pycache__` directories. They were removed only after resolving each target and confirming it was under the repository root.

## Known Warnings

- Harness validation still reports generated manifest source-fingerprint drift.
- Older raw queue statuses remain review-gated, and Harness doctor/self-check still point at Q09 review before Q14 can be accepted.
- AIDE Lite validates Q14 successfully but warns that the review packet is near the configured review-packet hard limit.
