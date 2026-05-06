# Q20 Validation

Interpreter: `py -3` / Python 3.11.9 unless noted.

## Baseline

- `git status --short`: PASS, clean before baseline commands.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with existing token-ledger near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, generated baseline snapshot.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, generated baseline repo/context maps.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 482 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 75 checked files, 5 changed files from baseline-generated artifacts, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, baseline review packet 6,900 chars / 1,725 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 73 total records, three near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, three near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, six golden tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, six pass / zero warn / zero fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, existing packet_too_large advisory class only.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, advisory recommendation only.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route class `local_strong`.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS, `.aide.local/` ignored and untracked.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, generated cache metadata only.
- `py -3 .aide/scripts/aide_lite.py gateway status`: PASS.
- `py -3 .aide/scripts/aide_lite.py gateway endpoints`: PASS.
- `py -3 .aide/scripts/aide_lite.py gateway smoke`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,626 chars / 907 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 6,900 chars / 1,725 approximate tokens after baseline refresh.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation.

Baseline generated churn was restored before Q20 edits.

## Final

Pending implementation.
