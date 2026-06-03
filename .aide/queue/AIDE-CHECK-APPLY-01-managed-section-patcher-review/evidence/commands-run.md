# Commands Run

## Inspection

- `git status --short --branch`: PASS
- `git log --oneline -50`: PASS
- `git remote -v`: PASS
- `git rev-parse HEAD`: PASS (`a775b1ac7b9a79c3196841e5475b225f2d676743`)
- `git rev-parse --show-toplevel`: PASS (`C:/Projects/AIDE/aide`)
- `git tag --list`: PASS (no tags listed)
- `git diff --check`: PASS
- `git check-ignore -v tmp/`: PASS (`.gitignore:30:/tmp/`)
- `git check-ignore -v tmp/*`: PASS (`.gitignore:30:/tmp/`)

## AIDE Validation

- `py -3 .aide/scripts/aide_lite.py doctor`: initial FAIL on stale managed-section validation report wording; rerun PASS after `managed-section fixture-verify` refreshed the report.
- `py -3 .aide/scripts/aide_lite.py validate`: initial FAIL on stale managed-section validation report wording; rerun PASS after `managed-section fixture-verify` refreshed the report.
- `py -3 .aide/scripts/aide_lite.py test`: PASS
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 171/171 golden tasks passed
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS
- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS, 333 checks
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-plan`: PASS
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS, 138 checks
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS
- `py -3 .aide/scripts/aide_lite.py transaction fixture-plan`: PASS
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS
- `py -3 .aide/scripts/aide_lite.py verify`: PASS
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS with expected `DIRTY_SOURCE_RECORDED` provenance before commit
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS
- `py -3 .aide/scripts/aide_lite.py capability validate`: PASS
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, 68 queue items; latest task packet points to AIDE-APPLY-02 as the assigned next task

## Unit Tests And Scans

- `py -3 -m unittest discover -s core/apply/tests -t .`: PASS, 10 tests
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_01_managed_sections.py`: PASS, 6 tests
- targeted high-confidence secret scan over modified and untracked files: PASS
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: pending post-commit validation
