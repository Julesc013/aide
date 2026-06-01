# Baseline State

- Repository: `C:/Projects/AIDE/aide`
- Remote: `https://github.com/Julesc013/aide.git`
- Branch: `main`
- Baseline commit: `eb100b4e315dd0fa1da5eaeed7ab2116d0c991a1`
- Baseline dirty state: clean before baseline validation commands.
- Starting branch state: `main...origin/main [ahead 1]`.

Baseline validation summary:

- `git status --short`: PASS, clean.
- `git diff --check`: PASS.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: PASS, 0 warnings.
- `py -3 scripts/aide doctor`: PASS, 0 warnings.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with pre-existing review-packet token warning.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 132/132.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN, pre-existing review-packet over hard limit.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, `DIRTY_SOURCE_RECORDED`.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 300 tests in about 607 seconds.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

