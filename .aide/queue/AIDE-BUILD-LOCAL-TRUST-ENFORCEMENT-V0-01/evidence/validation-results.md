# Validation Results

- PASS: `py -3 .aide\scripts\aide_lite.py local-trust fixture`
  - result: `PASS_WITH_WARNINGS`
  - evaluation_result: `allowed`
  - grant_consumed: `true`
  - concurrent_final_use_refused: `true`
  - idempotent_replay_no_second_event: `true`
  - all false-boundary fields remained false
- PASS: `py -3 .aide\scripts\aide_lite.py local-trust status`
  - result: `PASS_WITH_WARNINGS`
  - report_exists: `true`
- PASS: `py -3 .aide\scripts\aide_lite.py local-trust validate`
  - result: `PASS_WITH_WARNINGS`
  - validated: `true`
  - error_count: 0
- PASS: focused local trust tests
  - command: `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_trust_enforcement.py"`
  - result: 6 tests OK
- PASS: accepted trust contract regression tests
  - command: `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_trust_authorization_contract.py"`
  - result: 11 tests OK
- PASS: accepted local Service regression tests
  - command: `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_service_foundation.py"`
  - result: 7 tests OK
- PASS: `py -3 -m compileall core/service core/protocol .aide/scripts/tests`
- PASS: task inspect
  - classification: complete
  - missing_evidence: 0
- PASS: task evidence
  - evidence_files: 15
  - missing: none
- PASS: `py -3 .aide\scripts\aide_lite.py validate`
  - status: `PASS`
- PASS: `git diff --check`
- PASS: `git ls-files .aide.local`
  - output empty; no tracked `.aide.local` state
- PASS: new-surface absolute path scan
- PASS: new-surface secret-like scan

Notes:

- A broader historical scan over `PLANS.md`, `IMPLEMENT.md`, and the full
  `aide_lite.py` surfaced pre-existing absolute path and scanner-token text
  outside this task's new reports/evidence. The scoped Phase 10 task/report/code
  surfaces passed.
- Compile caches created by `compileall` were removed after validation.
- Generated git-helper plan churn from the preflight was restored before
  completion.
