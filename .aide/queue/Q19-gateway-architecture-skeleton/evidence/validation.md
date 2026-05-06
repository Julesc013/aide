# Q19 Validation

Interpreter: `py -3` / Python 3.11.9 unless noted.

## Baseline

- `git status --short`: PASS, clean before baseline commands.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings only.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings only.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, queue review-gate warnings only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with token-ledger near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote repo snapshot during baseline.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo/context maps during baseline.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote latest context packet during baseline.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN because generated eval run files were dirty from baseline and outside active scope.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, generated compact review packet during baseline.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS with budget warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS with budget warnings.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, six golden tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, six pass / zero warn / zero fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, packet_too_large recommendation class.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, advisory recommendation only.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route decision.
- `py -3 .aide/scripts/aide_lite.py cache init`: PASS.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, generated cache metadata during baseline.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 914 approx tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 1780 approx tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation.

Baseline generated churn was restored before Q19 edits.

## Final

Pending.
