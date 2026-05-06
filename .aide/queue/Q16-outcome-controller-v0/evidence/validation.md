# Q16 Validation Evidence

Interpreter used: Windows `py -3`.

## Baseline Before Editing

- `git status --short`: PASS, clean worktree before baseline commands.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 148 info, 7 warnings, 0 errors.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q09 through Q15 shown as `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, refreshed deterministic metadata snapshot with no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, refreshed repo-map/context-index metadata with no inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 1,930 chars / 483 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN only because baseline tests created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest review packet 6,222 chars / 1,556 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 48 current records, 49 total records, 0 budget warnings, 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, 49 records.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: WARN, 5 pass / 1 warn / 0 fail after review-packet regeneration.
- `py -3 .aide/scripts/aide_lite.py eval report`: WARN, 5 pass / 1 warn / 0 fail.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,223 chars / 806 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 6,222 chars / 1,556 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Final Validation

- `git status --short`: PASS, dirty only with Q16 implementation/docs/evidence/generated artifacts before final commit.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info / 7 warnings / 0 errors. Warnings are existing review-gate nuance and generated manifest source-fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same warning class as validate.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q16 shows `needs_review` / `implemented`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS; controller artifacts present and AGENTS managed section current.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS; 57 token ledger records before the manual smoke outcome, controller files present, latest task packet 804 approx tokens, review packet 1307 approx tokens, AGENTS current.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS; wrote `.aide/context/repo-snapshot.json`, 689 files, no inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS; wrote repo-map/test-map/context-index, 689 files, 628 heuristic test mappings, no inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS; latest context packet 1,936 chars / 484 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS; 38 changed files, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS; latest review packet 6,096 chars / 1,524 approximate tokens, verifier result PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS; 56 current records, 57 total records, 0 budget warnings, 0 regression warnings, no raw prompt/response storage.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS; largest surface was `AGENTS.md` at 2,590 approximate tokens; latest review packet 1,524 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger compare --baseline root_history_baseline --file .aide/context/latest-task-packet.md`: PASS; Q17 task packet 804 tokens vs 52,707 baseline tokens, 98.5 percent estimated reduction.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS; 6 golden tasks listed.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 6 PASS / 0 WARN / 0 FAIL; no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS; latest golden task result PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: PASS; outcome result PASS, 6 current records, 0 warnings, 0 failures.
- `py -3 .aide/scripts/aide_lite.py outcome add --phase Q16 --source validation --result PASS --failure-class unknown --severity info --notes "Q16 smoke outcome" --related-path .aide/queue/Q16-outcome-controller-v0/evidence/validation.md`: PASS; wrote metadata-only smoke outcome.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS; recommendation count 1, top recommendation `REC-PROCEED-Q17-WITH-GATES`, advisory only, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q17 Router Profile v0"`: PASS; latest task packet unchanged at 3,215 chars / 804 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 3,215 chars, 104 lines, 804 approximate tokens, within budget.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS; internal estimate/ignore/snapshot/index/context/pack/adapt/drift/line-ref/verifier/review-pack/ledger/eval/outcome/optimize/validate checks.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 55 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: expected documented failure; hidden `.aide` start directory is not importable with this top-level discovery shape.
- `git diff --check`: PASS; only line-ending conversion warnings from Git, no whitespace errors.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/test/template terms such as `api_key`, `SECRET`, `TOKEN`, path names, and fake test fixtures; no real provider key, credential, `.env` content, `.aide.local` state, or secret value was found.
- Post-evidence `py -3 .aide/scripts/aide_lite.py validate`: PASS; outcome ledger records 7 after the manual smoke outcome.
- Post-evidence `py -3 .aide/scripts/aide_lite.py verify`: PASS; 39 changed files, 0 warnings, 0 errors.

`PYTHONDONTWRITEBYTECODE=1` was set for final Python validation commands to avoid transient `__pycache__` directories entering changed-file verification.
